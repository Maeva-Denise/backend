from flask import Blueprint, request
import os, sys

from controllers.role import *
from .utils import parse_request_data
from .responses import JSONResponse

roles_view = Blueprint('roles', __name__, url_prefix='/roles')

@roles_view.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def list_or_create():
  if request.method == 'GET':
    return get_items()
  
  elif request.method in ['POST', 'PUT']:
    
    submitted_data = parse_request_data(request=request)
    state, msg = save_role(submitted_data)

  else:
    submitted_data = parse_request_data(request=request)
    state, msg = delete_role(submitted_data)

  if state:
    return msg
  else:
    return JSONResponse(f"<h1>{msg}</h1>", status=400)
    
