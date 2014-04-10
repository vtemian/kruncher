import os
import requests

from flask import Blueprint

from utils.decorators import validate, require
from utils.validators import validate_url

from .parser import Parser

endpoint = Blueprint('analyse_url', __name__)


@endpoint.route('analyse/', methods=['POST'])
@require('url')
@validate({
    'url': validate_url
})
def analyse_url(url):
  name, ext = os.path.splitext(url)
  parse = Parser(ext=ext[1:])

  response = requests.get(url, stream=True)
  fields = []
  for chunk in response.iter_lines(1024):
    fields = parse(chunk)
    if fields:
      break

  print fields

  return url
