
from email.policy import HTTP
import hashlib
import random
import string
from fastapi import APIRouter, HTTPException,Response,status
from auth import AuthHandler
from database.models.users import Users
from datetime import datetime
from datetime import timedelta
from database.otp_accessor import Otp_Accessor
from database.users_accsesor import User_Accessor

from email_sender import EmailSender

class Opt_service:
    def __init__(self,otp_accessor : Otp_Accessor,users_accessor:User_Accessor)-> None:
        self.accessor = otp_accessor
        self.users_accessor = users_accessor
        print(users_accessor.name)
    
    def get_row_using_email(self , email :str):
        return self.users_accessor.get_row_using_email(email)
    def get_row_using_otp(self , otp :str):
        return self.accessor.get_row_using_otp(otp)
    def delete_row_using_otp(self , otp :str):
        self.accessor.delete_row_using_otp(otp)
    def add_otp_row(self , otp :str,user_id :int,expiration_date :datetime):
        self.accessor.add_opt_row(otp,user_id,expiration_date)
    def delete_every_row_that_is_expired(self):
        self.accessor.delete_every_row_that_is_expired()


class Otp_router(APIRouter):
    def __init__(self,service:Opt_service,name:str=""):
        super().__init__()
        self.email_sender = EmailSender()
        self.service = service
        self.name = name
        self.add_api_route("/email_sent",endpoint=self.email_sent,methods = ["POST"])

    def six_digit_otp(self):
        return ''.join(random.choice(string.digits) for i in range(6))

    async def email_sent(self,email:str,response:Response):
        #TODO:serch for email in the opt table
        user:Users = self.service.get_row_using_email(email)#TODO: implement the get user with email
        print(user)
        if user is None:
            return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='there is no user with this email')
        otp = self.six_digit_otp()
        print(otp)
        #check that the otp is not already in the database
        while self.service.get_row_using_otp(otp):
            otp = self.six_digit_otp()
        self.service.add_otp_row(otp,user.id,datetime.now()+timedelta(minutes=20))
        # self.email_sender.send_email(email,otp)
        response.status_code = status.HTTP_200_OK
        return {"status":"the email was sent"}