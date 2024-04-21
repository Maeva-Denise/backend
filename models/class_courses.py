import sqlite3 as sq
from .constants import PATH_TO_DB
from .base_model import *
from .classes import Class
from .courses import Courses

class classCourse(Shared_Model, AbstractBaseModel):
  
  table = 'class_courses'

  def __init__(self, class_id=None, course_id=None, course_info=None) -> None:
    super().__init__(self.table)
    cls_obj = Class()
    course_obj = Courses()

    if class_id:
      state, item = cls_obj.read_unique(column="class_id", data=class_id)
      self.class_name = (item.toJSON())['class_name'] if state else None

    if course_id:
      state, item = course_obj.read_unique(column="course_id", data=class_id)
      self.course_name = (item.toJSON())['course_name'] if state else None

    self.course_info = course_info

  def create(self):
    try:

      with sq.connect(PATH_TO_DB) as conn:
        cur = conn.cursor()

        # Enable foreign key support 
        cur.execute('PRAGMA foreign_keys = ON')
      
        # Create the course information table
        query = '''CREATE TABLE IF NOT EXISTS class_courses (
          class_id INTEGER,
          course_id INTEGER,
          course_info TEXT,
          PRIMARY KEY(class_id, course_id)
        )'''
        cur.execute(query)
        conn.commit()

        return True, ''
      
    except sq.Error as err:
      return False, err
    
    finally:
        conn.close()


  def write(self, data_list, set_type = False):
    try:
      with sq.connect(PATH_TO_DB) as conn:
        cur = conn.cursor()

        if set_type:
          query = f"INSERT INTO {self.table} VALUES(?, ?, ?)"
          cur.execute(query, data_list)

        else:
          for row in data_list:
            query = f"INSERT INTO {self.table} VALUES(?, ?, ?)"
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
          file = __class__(class_id=row[0], course_id=row[1], course_info=row[2])
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

        file = __class__(class_id=result[0], course_id=result[1], course_info=result[2])

        return True, file
    
    except sq.Error as e:
      return False, e
    
    finally:
      conn.close()

  def update(self, set_data, class_id, course_id):
    try:
      with sq.connect(PATH_TO_DB) as conn:
        cur = conn.cursor()

        update = f"UPDATE {self.table} set course_info = '{set_data}' WHERE class_id = {class_id} AND course_id = {course_id}"
        
        cur.execute(update)
        conn.commit()
        
        return True, 'Update successful'

    except sq.Error as err:
      return False, err
    
    finally:
      conn.close()


  def toJSON(self):
    return {
      "class_name": self.class_name,
      "course_name": self.course_name,
      "course_info": self.course_info
    }