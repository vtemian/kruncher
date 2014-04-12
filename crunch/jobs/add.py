import sys
import rethinkdb as r
from disco.core import Job
import csv


class GroupSum(Job):
  def __init__(self, group_by, fields, *args, **kwargs):
    self.group_by = int(group_by)
    self.fields = map(int, fields)

    super(GroupSum, self).__init__(*args, **kwargs)

  @staticmethod
  def map_reader(fd, size, url, params):
    reader = csv.reader(fd, delimiter=',')
    for row in reader:
      if len(row) <= 1:
        continue
      yield row

  def map(self, line, params):
    words = line
    total = 0
    result = []
    for word in range(len(words)):
      if word == self.group_by:
        continue
      try:
        if word in self.fields:
          total += int(words[word])
        else:
          result.append(int(words[word]))
      except:
        pass

    result.insert(0, total)

    yield words[self.group_by], result

  def reduce(self, rows_iter, out, params):
    from disco.util import kvgroup
    final = {}
    for key, result in kvgroup(rows_iter):
      if key not in final:
         final[key] = []
      for line in result:
        for value in range(len(line)):
          if len(final[key]) <= value:
            final[key].append(line[value])
          else:
            final[key][value] += line[value]
    out.add(final, "a")

if __name__ == '__main__':
  from add import GroupSum
  db = r.connect(**{
      'host': 'batman.krunchr.net',
      'port': 28019,
      'auth_key': '',
      'db': 'krunchr'
  })
  dataset = r.db("krunchr").table('datasets').get(sys.argv[1]).run(db)

  fields = [str(dataset['fields'].index(field)) for field in sys.argv[2:]]
  group_by = dataset['fields'].index(sys.argv[2])

  job = GroupSum(group_by, fields)
  job.run(input=['data:%s' % sys.argv[1]])

  from disco.core import result_iterator

  table_name = sys.argv[1].replace('-', '_')
  try:
    r.db("krunchr").table_create(table_name).run(db)
  except:
    pass
  lines = []
  fields = dataset['fields']
  fields.remove(sys.argv[2])
  for line in result_iterator(job.wait(show=True)):
    for key in line[0]:
      insert = {sys.argv[2]: key}
      if len(line[0][key]) < len(fields):
 	continue
      insert.update({field: line[0][key][fields.index(field)-1] for field in fields})
      r.table(table_name).insert(insert).run(db)

  r.table('datasets').filter({'id': sys.argv[1]}).update({'ready': True}).run(db)
