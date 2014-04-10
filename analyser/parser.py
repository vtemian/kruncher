class Parser(object):
  def __init__(self, ext=None):
    self.ext = ext
    self.PARSERS = {
        'csv': lambda chunk: chunk.split(","),
        'csv_tab': lambda chunk: chunk.split("\t"),
        'txt': lambda chunk: chunk.split(" ")
    }

  def __call__(self, chunk):
    fields = self.PARSERS[self.ext](chunk)

    if not fields:
      for key in self.PARSERS:
        fields = self.PARSERS[key]
        if fields:
          break

    return fields
