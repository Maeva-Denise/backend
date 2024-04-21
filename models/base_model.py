from abc import ABC, abstractmethod
import json
import sqlite3 as sq
from .constants import PATH_TO_DB

class AbstractBaseModel(ABC, dict):
    def __init__(self) -> None:
        self.id = None
        super().__init__()
    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def read(id=None):
        pass

    @abstractmethod
    def delete(self):
        pass

    def __str__(self):
        return f"BaseModel {self.id}"
    

class Shared_Model:
  table = None
  
  def __init__(self, table=None ) -> None:
    self.table = table  

  def update(self, column, setInfo, value):

    try:
      with sq.connect(PATH_TO_DB) as conn:
        cur = conn.cursor()

        if column in ['id', 'course_id', 'class_id']:
          update = f"UPDATE {self.table} set {setInfo} WHERE {column} = {value}"

        else:
          update = f"UPDATE {self.table} set {setInfo} WHERE {column} = '{value}'"

        cur.execute(update)
        conn.commit()
        
        return True, 'Update successful'

    except sq.Error as err:
      return False, err
    
    finally:
      conn.close()
    

  def delete(self, condition=None):
    try:
       with sq.connect(PATH_TO_DB) as conn:
        cur = conn.cursor()

        if condition:
          query = f"DELETE FROM {self.table} WHERE {condition}"

        else:
          query = f"DELETE FROM {self.table}"

        if cur.execute(query):
          conn.commit()
          return True, 'Delete successful'
        
        return False, "Delete Failed"

    except sq.Error as e:
      return False, e
    
    finally:
      conn.close()
