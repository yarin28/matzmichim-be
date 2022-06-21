import datetime
from sqlalchemy.orm import Session
from database.accessor import Accessor
from database.models.admins import admins
from sqlalchemy import DateTime, String
from typing import List
from enum import Enum

class User_Accessor(Accessor):
    """
    the connector between the database and the python server. Has a lot of
    functions to provide the different routers with the options that they need
    for pulling data from the database.

    per table accessors are created for the different tables.
    """
    def __init__(self,session:Session, model):
        Accessor.__init__(self,session,model)   
        self.name="users accessor"
    
    # get user with the right username
    def get_user(self,id:int):
        return self.session.query(self.model).filter(self.model.id == id).first()
       
    # add user according to the users table
    def add_user(self,id:String,email:String,full_name:String,phone:String):
        self.add(self.model(id = id,email = email,full_name = full_name,phone = phone))


    def commit(self):
        self.session.commit()

    def get_row_using_email(self,email:String):
        row = self.session.query(self.model).filter(self.model.email == email).all()#HACK:replace the filter with get for performance?
        print(row)
        if len(row) >1:
            return None
        return row[0] #HACK: should be a list with one element
