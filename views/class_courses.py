from flask import Blueprint, request
import os, sys

from controllers.class_courses import *
from .utils import parse_request_data
from .responses import JSONResponse

class_course_view = Blueprint('class_course', __name__, url_prefix='/class_courses')

@class_course_view.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def list_or_create():
  if request.method == 'GET':
    if request.args.get('condition'):
      
      return get_items(cond=request.args.get('condition'))
    
    return get_items()
  elif request.method in ['POST', 'PUT']:
    
    submitted_data = request.json

    state, msg = save_courseInfo(submitted_data)

  else:
    submitted_data = parse_request_data(request=request)
    state, msg = delete_courseinfo(submitted_data)

  if state:
    return msg
  else:
    return JSONResponse(f"<h1>{msg}</h1>", status=400)
    
