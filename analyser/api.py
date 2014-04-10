from flask.ext.classy import FlaskView

from utils.decorators import validate, require
from utils.validators import validate_url


class AnalyserView(FlaskView):
  @require('url')
  @validate({
      'url': validate_url
  })
  def post(self, url):
    return url
