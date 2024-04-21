from flask import Blueprint, request
import os, sys

from controllers.students import *
from .utils import parse_request_data
from .responses import JSONResponse

students_view = Blueprint('students', __name__, url_prefix='/students')

@students_view.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def list_or_create():
  if request.method == 'GET':
    if request.args.get('condition'):
      
      return get_items(cond=request.args.get('condition'))
    
    return get_items()
  
  elif request.method in ['POST', 'PUT']:
    
    submitted_data = parse_request_data(request=request)
    state, msg = save_student(submitted_data)

  else:
    submitted_data = parse_request_data(request=request)
    state, msg = delete_student(submitted_data)

  if state:
    return msg
  else:
    return JSONResponse(f"<h1>{msg}</h1>", status=400)
    
