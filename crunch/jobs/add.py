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

def try_me(argv):
  db = r.connect(**{
      'host': 'batman.krunchr.net',
      'port': 28019,
      'auth_key': '',
      'db': 'krunchr'
  })
  job = GroupSum(argv[1], argv[1:])
  job.run(input=['data:%s' % argv[0]])

  from disco.core import result_iterator

  lines = []
  for line in result_iterator(job.wait(show=True)):
    lines.append(line)
