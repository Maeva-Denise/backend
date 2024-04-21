from flask import Blueprint, request
import os, sys

from controllers.courses import *
from .utils import parse_request_data
from .responses import JSONResponse

courses_view = Blueprint('courses', __name__, url_prefix='/courses')

@courses_view.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def list_or_create():
  if request.method == 'GET':
    if request.args.get('condition'):
      
      return get_items(cond=request.args.get('condition'))

    return get_items()
  
  elif request.method in ['POST', 'PUT']:
    submitted_data = parse_request_data(request=request)
    state, course = save_course(submitted_data)

  else:
    submitted_data = parse_request_data(request=request)
    state, course = delete_course(submitted_data)


  if state:
    return course
  else:
    return JSONResponse(f"<h1>{course}</h1>", status=400)
    
