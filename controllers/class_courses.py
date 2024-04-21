import os
import sys
current_dir = os.getcwd()
sys.path.append(current_dir)

from models.class_courses import classCourse
from models.courses import Courses
from models.classes import Class

obj = classCourse()

column_list = ['class_id', 'course_id', 'course_info']
def get_items(cond = None, return_obj=False):

  if cond is None:
    status, items = obj.read()

  else:
    status, items = obj.read(cond)

  if status:
    if not return_obj:
      list_of_items = [
        item.toJSON() for item in items
      ]
      return list_of_items
    
    return items

  else:
    return None

def get_unique_item(col, data, return_obj = False):

  status, item = obj.read_unique(column=col, data=data)

  if status and not return_obj:
    return status, item.toJSON

  return status, item

def save_courseInfo(item_dict): 

  # A new class_course record cannot be added, only the course_info field can be updated

  state, msg = data_verify(item_dict)

  if not state:
    return state, msg
      
  # Update the db

  return obj.update(set_data=item_dict['course_info'], class_id=item_dict['class_id'], course_id=item_dict['course_id'])


def data_verify(item_dict):
  global column_list

  if len(item_dict) > 3 or len(item_dict) < 3:
    return False, "column count doesn't match"

  # Ensure there are no unknown columns
  print(column_list)
  print(item_dict.keys())

  for key in item_dict.keys():
    if key not in column_list:
      return False, f"Invalid key, {key}"
  
  # Ensure that a unique columns are present
  if 'course_id' not in item_dict: 
    return False, "You must give a course to be updated"

  if 'class_id' not in item_dict: 
    return False, "A class must be given"
  
  if 'course_info' not in item_dict: 
    return False, "There is no information to update"
  
  # Verify that the given class and course exists
  if not isExist(value=item_dict['class_id'], table="class"):
    return False, "Invalid Class"
  
  if not isExist(value=item_dict['course_id'], table="courses"):
    return False, "Invalid Course"
  
  return True, ''
  

def isExist(value, table):

  if table == "class":
      new_obj = Class()
      column = "class_id"

  else:
    new_obj = Courses()
    column = "course_id"

  stats = new_obj.read_unique(column, data=value)

  if stats[0]:
    return True

  else:
    return False


def delete_courseinfo(item_dict):
  state, msg = data_verify(item_dict)

  if not state:
    return state, msg
    
  condition = f"class_id = {item_dict['class_id']} AND course_id = {item_dict['course_id']}"

  return obj.delete(condition)