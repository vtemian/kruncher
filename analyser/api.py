from flask import Blueprint

from utils.decorators import validate, require
from utils.validators import validate_url

endpoint = Blueprint('analyse_url', __name__)


@endpoint.route('analyse/', methods=['POST'])
@require('url')
@validate({
    'url': validate_url
})
def analyse_url(url):
  print url
  return url
