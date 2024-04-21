import sqlite3 as sq
import os, sys
current_dir = os.getcwd()
sys.path.append(current_dir)

from .base_model import *
from .constants import PATH_TO_DB
from .classes import Class
from .role import Role

class Students(Shared_Model, AbstractBaseModel):
  
  table = 'students'

  def __init__(self, id=None, name=None, Dob=None, gender=None, Tel=None, role=None, class_id=None):

    super().__init__(self.table)
    role_obj = Role()
    cls_obj = Class()
    self.id = id
    self.name = name
    self.Dob = Dob,
    self.gender = gender
    self.Tel = Tel
    self.role = role
    self.class_id = class_id

  def create(self):
    try:

      with sq.connect(PATH_TO_DB) as conn:
        cur = conn.cursor()
      
        # Enable foreign key support 
        cur.execute('PRAGMA foreign_keys = ON')

        # Create role table
        query = '''CREATE TABLE IF NOT EXISTS students (
          id INTEGER PRIMARY KEY, 
          name varchar(50) UNIQUE COLLATE NOCASE,
          Dob DATE,
          gender char(2) CHECK(gender IN('M', 'F')),
          Tel varchar(12),
          role_id INTEGER default 2,
          class_id INTEGER,
          FOREIGN KEY(role_id) REFERENCES role(role_id),
          FOREIGN KEY(class_id) REFERENCES role(class_id)
          
        )'''
        cur.execute(query)
        conn.commit()

        return True, 'Table created successfully'
      
    except sq.Error as err:
      return False, err
    
    finally:
        conn.close()


  def write(self, data_list, set_type = False):
    try:
      with sq.connect(PATH_TO_DB) as conn:
        cur = conn.cursor()

        if set_type:
          query = f"INSERT INTO {self.table} VALUES(?, ?, ?, ?, ?, ?, ?)"
          cur.execute(query, data_list)

        else:
          for row in data_list:
            query = f"INSERT INTO {self.table} VALUES(?, ?, ?, ?, ?, ?, ?)"
            cur.execute(query, row)

        conn.commit()

        return True, 'Insert Successful'

    except sq.Error as err:
      return False, err
    
    finally:
      conn.close()
  
  def read(self, condition=None):
    try:
      with sq.connect(PATH_TO_DB) as conn:
        cur = conn.cursor()

        files = []
        if condition:
          query = f"SELECT * FROM {self.table} WHERE {condition}"
        
        else:
          query = f"SELECT * FROM {self.table}"

        result = cur.execute(query).fetchall()
        
        if not result:
          return False, "No Result found"

        for row in result:

          file = __class__(id=row[0], name=row[1], Dob=row[2], gender=row[3], Tel=row[4], role=row[5], class_id=row[6])
          files.append(file)

        return True, files

    except sq.Error as e:
      return False, e
    
    finally:
      conn.close()

  def read_unique(self, column, data):
    try:
      with sq.connect(PATH_TO_DB) as conn:
        cur = conn.cursor()

        query = f"SELECT * FROM {self.table} WHERE {column} = '{data}'"
        result = cur.execute(query).fetchone()

        if not result:
          return False, "No Result found"

        file = __class__(id=result[0], name=result[1], Dob=result[2], gender=result[3], Tel=result[4], role=result[5], class_id=result[6])

        return True, file
    
    except sq.Error as e:
      return False, e
    
    finally:
      conn.close()
  
  def toJSON(self):
    return {
      "id": self.id,
      "name": self.name,
      "Dob": (self.Dob)[0],
      "gender": self.gender,
      "Tel": self.Tel,
      "role_id": self.role,
      "class_id": self.class_id
    }
