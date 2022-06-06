import datetime
from sqlalchemy.orm import Session
from database.accessor import Accessor
from database.models.admins import admins
from sqlalchemy import DateTime
from typing import List
from enum import Enum

class User_Accessor(Accessor):
    """
    the connector between the database and the python server. Has a lot of
    functions to provide the different routers with the options that they need
    for pulling data from the database.

    per table accessors are created for the different tables.
    """
    def __init__(self,session:Session, model ):
        Accessor.__init__(self,session,model)   
    

    #TODO: only for the users table -> should be moved to a different accsesor
    def get_user(self,name:str):
        return rows
       

    def add_user(self,name:str,hashed_password:str):
        self.session.add(self.model(username=name,password = hashed_password))
        self.session.commit()
