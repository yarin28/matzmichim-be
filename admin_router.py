
import csv
import hashlib
import json
from io import StringIO
from fastapi import APIRouter, Form, HTTPException,Response,status, UploadFile,File
from auth import AuthHandler
from csv_Handler import CsvHandler
from database.users_accsesor import User_Accessor
from database.accessor import Accessor
from database.admins_accessor import Admin_Accessor

class AdminService:
    """
    the login class is used to access the users table inside the database. It is a
wrapper to the asscessor and features many different functions to deal with the
users and passwords. It supplies the programmer an easy way to work with the
users table.
    """
    def __init__(self,admin_accessor : Admin_Accessor,users_accessor :User_Accessor)-> None:
        self.admin_accessor = admin_accessor
        self.users_accessor = users_accessor

    def get_user(self , Id :str):
        return self.users_accessor.get_user(Id)
    def get_all_admins(self):
        return self.admin_accessor.get_all()
    def get_all_users(self):
        return self.users_accessor.get_all()

    def add_user(self,Id:str,email:str,full_name:str,phone:str):
        self.users_accessor.add_user(Id,email,full_name,phone)
        return True
    def commit_users_table(self):
        self.users_accessor.commit()
    def check_password(self,username:str,password:str):
        user = self.get_user(username)
        if user is None:
            return False
        user_password = user.password

        if user_password is None:
            return False
        return user_password == hashlib.sha256(salt.encode() + password.encode()).hexdigest()
    

class AdminRouter(APIRouter):
    def __init__(self,service:AdminService,name:str="",auth_handler:AuthHandler=None):
        super().__init__()
        self.auth_handler = auth_handler
        self.service = service
        self.name = name
        self.add_api_route("/sign_up",endpoint=self.sign_up,methods = ["POST"])
        self.add_api_route("/login",endpoint=self.login,methods = ["POST"])
        
        #newly added
        self.add_api_route("/register",endpoint=self.register,methods = ["POST"],status_code=201)
        self.add_api_route("/validate_csv",endpoint=self.validate_csv,methods = ["POST"],status_code=201)
        self.add_api_route("/upload_csv",endpoint=self.upload_csv,methods = ["POST"],status_code=201)


    async def register(self,username:str,password:str,response:Response):
        if any(x.username == username for x in self.service.get_all()):
            response.status_code = status.HTTP_406_NOT_ACCEPTABLE
            return False
        hashed_password = self.auth_handler.get_password_hash(password)
        self.service.add_user(username,hashed_password)
        return{}
    
    async def sign_up(self,username:str,password:str,response:Response):
        if self.service.add_user(username,password):
            response.status_code = status.HTTP_201_CREATED
            return True
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return False

    async def login(self,username:str,password:str,response:Response):
        user = None
        for x in self.service.get_all():
            if x.username == username:
                user = x
                break
        if user is None or (not self.auth_handler.verify_password(password,user.password)):
            raise HTTPException(status_code=401, detail='Invalid username or password')
        token = self.auth_handler.encode_token(username)
        return {'token':token}

    async def validate_csv(self,file:UploadFile = File(...)):
        
        contents = await file.read()
        decoded = contents.decode()
        buffer = StringIO(decoded)
        rows = csv.DictReader(buffer)
        data = self.validate_rows( rows)
        buffer.close()
        return data

    def validate_rows(self, rows):
        data = []
        for row in rows:             
            row =  CsvHandler.validate_row(row)
            data.append(row) 
        return data

    def update_users_rows(self,rows):
        data = []
        for row in rows:
            if  row['RESULT'] == []:
                user = self.service.get_user(row['ID'])
                if user is not None:
                    # row['RESULT'].append({'UPDATE':[]})
                    for key,value in row.items():
                        if key.lower() in user.__dict__.keys():
                            if value != user.__dict__[key.lower()] :

                                row['RESULT'].append({'UPDATED':key,
                                'OLD_VALUE':user.__dict__[key.lower()],
                                'NEW_VALUE':row[key]})
                            setattr(user,key.lower(),value)
            data.append(row)
        return data

    def add_users_rows(self,rows):
        data = []
        for row in rows:
            if  row['RESULT'] == []:
                if self.service.get_user(row['ID']) is None:
                    row["RESULT"].append({"ADDED":"added"})
                    self.service.add_user(row["ID"],row["Email"],row["Full_name"],row["Phone"])
                else:
                    row["RESULT"].append({"NOTHING":"already exists"})
            data.append(row)
        return data

    async def upload_csv(self,response:Response,course_name:str = Form(...), course_short_desc:str=Form(...) , file:UploadFile = File(...)):
        print(response)
        contents = await file.read()
        decoded = contents.decode()
        buffer = StringIO(decoded)
        csvReader = csv.DictReader(buffer)
        data = []
        data = self.validate_rows(csvReader)
        data = self.update_users_rows(data)
        data = self.add_users_rows(data)

        for row in self.service.get_all_users():
            print(row.__dict__)
        self.service.commit_users_table()
        buffer.close()
        return data