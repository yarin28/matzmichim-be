import hashlib
from fastapi import APIRouter, HTTPException,Response,status
from auth import AuthHandler
from database.accessor import Accessor

salt = '603aa9c25024402b96b8b477cf515bf9'
class LoginService:
    """
    the login class is used to access the users table inside the database. It is a
wrapper to the asscessor and features many different functions to deal with the
users and passwords. It supplies the programmer an easy way to work with the
users table.
    """
    def __init__(self,accsesor : Accessor)-> None:
        self.accsesor = accsesor

    def get_user(self , name :str):
        return self.accsesor.get_user(name)
    def get_all(self):
        return self.accsesor.get_all()

    def add_user(self,name:str,password:str):
        self.accsesor.add_user(name,password)
        return True
    
    def check_password(self,username:str,password:str):
        user = self.get_user(username)
        if user is None:
            return False
        user_password = user.password

        if user_password is None:
            return False
        return user_password == hashlib.sha256(salt.encode() + password.encode()).hexdigest()
    

class LoginRouter(APIRouter):
    def __init__(self,service:LoginService,name:str="",auth_handler:AuthHandler=None):
        super().__init__()
        self.auth_handler = auth_handler
        self.service = service
        self.name = name
        self.add_api_route("/sign_up",endpoint=self.sign_up,methods = ["POST"])
        self.add_api_route("/login",endpoint=self.login,methods = ["POST"])
        
        #newly added
        self.add_api_route("/register",endpoint=self.register,methods = ["POST"],status_code=201)

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
