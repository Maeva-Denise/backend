import sqlite3 as sq
from .base_model import *
from .constants import PATH_TO_DB

class Role(Shared_Model, AbstractBaseModel):
  
  table = 'role'

  def __init__(self, id=None, name=None) -> None:
    super().__init__(self.table)

    self.id = id
    self.name = name


  def create(self):
    try:
      with sq.connect(PATH_TO_DB) as conn:
        cur = conn.cursor()
      
        # Create role table
        query = f"CREATE TABLE IF NOT EXISTS {self.table} (role_id INTEGER PRIMARY KEY, role_name varchar(15) UNIQUE)"

        cur.execute(query)
        conn.commit()

        return True, 'Table Created successfully'
      
    except sq.Error as err:
      return False, err
    
    finally:
      conn.close()
    

  def write(self, data_list, set_type = False):
    try:
      with sq.connect(PATH_TO_DB) as conn:
        cur = conn.cursor()

        if set_type:
          insert = f"INSERT INTO {self.table} VALUES (?, ?)"
          cur.execute(insert, data_list)

        else:

          for row in data_list:
            insert = f"INSERT INTO {self.table} VALUES (?, ?)"
            cur.execute(insert, row)

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

          file = __class__(id=row[0], name=row[1])
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

        file = __class__(id=result[0], name=result[1])

        return True, file
    
    except sq.Error as e:
      return False, e
    
    finally:
      conn.close()

  def toJSON(self):
    return {
      "role_id": self.id,
      "role_name": self.name
    }