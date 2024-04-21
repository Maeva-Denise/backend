import os
import sys
current_dir = os.getcwd()
sys.path.append(current_dir)

from models.role import Role

obj = Role()

column_list = ['role_id', "role_name"]

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


def save_role(item_dict):
  state, msg = data_verify(item_dict)

  if not state:
    return state, msg
  
  if isExist(item_dict['role_id']):
    if class_name == item_dict['role_name']:
      return False, "There is nothing to update"
    
    else:
      # update the db
      return update_role(item_dict, column="role_id", unq_value=item_dict['role_id'])
  
  elif get_unique_item(col="role_name", data=item_dict['role_name'])[0]:
    return False, "Role already exists"
  
  else:
    # Insert into the db
    return insert(item_dict)
  

def data_verify(item_dict):
  global column_list

  if len(item_dict) != 2 :
    return False, "column count doesn't match"
  
  # Ensure there are no unknown columns
  for key in item_dict.keys():
    if key not in column_list:
      return False, f"Invalid key, {key}"
  
  # Ensure that a unique column is present
  if 'role_id' not in item_dict:
    return False, "A Unique column must be present"

  if 'role_name' not in item_dict:
    return False, "A role column must be included"
  
  return True, ''


def isExist(value):
  global class_name

  stats, items = get_unique_item(col="class_id", data=value)

  if stats:
    class_name = items['class_name']
    return True
  
  else:
    return False
  
  
def update_role(item_dict, column, unq_value):
  setInfo = f"class_name = {item_dict['class_name']}"
  return obj.update(column, setInfo, unq_value)
    

def insert(dict):
  global column_list

  for col in column_list:
    if col not in list(dict.keys()):
      dict[col] = None
  
  dict['class_id'] = None

  # sort the keys in db order 
  dict = {key : dict[key] for key in column_list}
  value_tuple = tuple(dict.values())
  
  return obj.write(value_tuple, set_type=True) 


def delete_role(item_dict):
  state, msg = data_verify(item_dict)

  if not state:
    return state, msg
  
  id = item_dict['role_id']
  condition = f"role_id = {id}"

  return obj.delete(condition)