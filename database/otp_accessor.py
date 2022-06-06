import datetime
from sqlalchemy.orm import Session
from database.accessor import Accessor
from database.models.admins import admins
from sqlalchemy import DateTime
from typing import List
from enum import Enum

class Otp_Accessor(Accessor):
    """
    the connector between the database and the python server. Has a lot of
    functions to provide the different routers with the options that they need
    for pulling data from the database.

    per table accessors are created for the different tables.
    """
    def __init__(self,session:Session, model):
        Accessor.__init__(self,session,model)   
    # get user with the right opt
    def get_row_using_otp(self,otp:str):
       return self.session.query(self.model).filter(self.model.otp == otp).first()
       
    def delete_row_using_otp(self,otp:str):
        self.session.delete(self.get_row_using_otp(otp))
        self.session.commit()
    
    def add_opt_row(self,otp:str,user_id:int,session_end:datetime):
        self.add(self.model(otp = otp,user_id = user_id,session_end = session_end))
    def delete_every_row_that_is_expired(self):
        self.session.query(self.model).filter(self.model.session_end < datetime.datetime.now()).delete()
        self.session.commit()

        