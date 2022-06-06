import datetime
from sqlalchemy.orm import Session
from database.models.admins import admins
from sqlalchemy import DateTime
from typing import List
from enum import Enum

class Accessor:
    """
    the connector between the database and the python server. Has a lot of
    functions to provide the different routers with the options that they need
    for pulling data from the database.

    per table accessors are created for the different tables.
    """
    def __init__(self,session:Session, model ):
        self.session = session
        self.model = model
    
    def get_all(self):
        return self.session.query(self.model).all()



    def add(self,obj):
        self.session.add(obj)
        self.session.commit()

