import os
import sys
current_dir = os.getcwd()
sys.path.append(current_dir)

from models.students import Students
from models.role import Role
from models.classes import Class

obj = Students()

column_list = ['id', 'name', 'Dob', 'gender', 'Tel', 'role', 'class']

def get_items(cond = None, return_obj=False):
  if cond is None:
    status, students = obj.read()

  else:
    status, students = obj.read(cond)

  if status:
    if not return_obj:
      list_of_students = [
        stud.toJSON() for stud in students
      ]
      
      return list_of_students
    
    return students

  else:
    return None


def get_unique_item(col, data, return_obj = False):
  status, student = obj.read_unique(column=col, data=data)

  if status and not return_obj:
    return status, student.toJSON

  return status, student


def save_student(item_dict):
  state, msg = data_verify(item_dict)

  if not state:
    return state, msg
  
  update = update_id = False
  if 'id' in item_dict:
    # Verify if the id exists in the db
    id = item_dict['id']
    status, exist_course = get_unique_item(col="id", data=id, return_obj=True)

    if status:
      update = update_id = True
      
  if not update:
    if 'name' in item_dict:
      # Check for the course_name
      name = item_dict['name']
      status, exist_course = get_unique_item(col="name", data=name, return_obj=True)

      if status:
        update = True

  if not update:
    # Insert into the db
    return insert(item_dict)
    
  else:
    # Update the db
    if update_id:
      return update_student(item_dict, "id", id)
    
    else:
      return update_student(item_dict, "name", name)


def data_verify(item_dict):
  global column_list

  if len(item_dict) > 7 or len(item_dict) < 2 :
    return False, "column count doesn't match"
  
  # Ensure there are no unknown columns
  for key in item_dict.keys():
    if key not in column_list:
      return False, f"Invalid key, {key}"
  
  # Ensure that a unique column is present
  if 'id' not in item_dict:
    if 'name' not in item_dict:
      return False, "A Unique column must be present"

  # Ensure that the role presented is either a Delegate or a student
  if 'role' in item_dict:
    if not isExist(value=item_dict['role'], table="role"):
      return False, "Invalid role"

  # for class
  if 'class' in item_dict:
    if not isExist(value=item_dict['class'], table="class"):
      return False, "Invalid Class"
    
  return True, ''


def isExist(value, table):
  global info_class_id, info_role_id

  if table == "class":
      new_obj = Class()

  else:
    new_obj = Role()

  stats, items = new_obj.read()

  if stats:
    list_of_items = [
        item.toJSON() for item in items
      ]
    
    for data in list_of_items:
      new_item = list(data.values())

      if new_item[1] == value:
        if table == "class":
          info_class_id = new_item[0]

        else:
          info_role_id = new_item[0]

        return True

    return False
    
  else:
    return False
  
  
def update_student(item_dict, column, unq_value):
  setInfo = ""
  length = 1
  for key, value in item_dict.items():
    if key == "role":
      key = "role_id" 
      value = info_role_id
    
    elif key == "class":
      key = "class_id"
      value = info_class_id

    if length == len(item_dict):
      setInfo += f"{key} = '{value}' "
    
    else:
      setInfo += f"{key} = '{value}', "

    length += 1

  return obj.update(column, setInfo, unq_value)
    

def insert(dict):
  global column_list

  for col in column_list:
    if col not in list(dict.keys()):
      dict[col] = None
  
  dict['id'] = None
  dict['role'] = info_role_id
  dict['class'] = info_class_id

  # sort the keys in db order 
  dict = {key : dict[key] for key in column_list}
  value_tuple = tuple(dict.values())
  
  return obj.write(value_tuple, set_type=True) 


def delete_student(item_dict):
  state, msg = data_verify(item_dict)

  if not state:
    return state, msg
  
  if 'id' in item_dict:
    id = item_dict['id']
    condition = f"id = {id}"

  else:
    name = item_dict['name']
    condition = f"name = '{name}'"

  return obj.delete(condition)