from disco.core import Job


class GroupSum(Job):
  def __init__(self, group_by, fields, *args, **kwargs):
    self.group_by = group_by
    self.fields = fields

    super(GroupSum, self).__init__(*args, **kwargs)

  def map(self, line, params):
    "vlad,12,1,3,4"
    words = line.split(',')
    total = 0
    result = []
    for word in range(len(words)):
      if word in self.fields:
        total += int(words[word])
      else:
        result.append(int(words[word]))

    result.insert(total, 0)
    yield words[self.group_by], result

  def reduce(self, rows_iter, out, params):
    from disco.util import kvgroup
    for key, result in kvgroup(rows_iter):
      final = []
      for line in range(result):
        for value in range(line):
          if len(final) < value:
            final.append(line[value])
          else:
            final[value] += line[value]
        yield key, final
