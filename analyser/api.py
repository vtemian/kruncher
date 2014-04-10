from flask.ext.classy import FlaskView


class AnalyserView(FlaskView):
  def get(self):
    return "awesome"
