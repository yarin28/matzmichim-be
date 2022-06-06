import os
from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from multiprocessing import Process
from uvicorn import run
from asyncio import sleep
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from auth import AuthHandler
from database.models.admins import admins
from database.admins_accessor import Admin_Accessor
from database.models.otp_session import OTP_Session
from database.models.users import Users
from database.accessor import Accessor
from fastapi.middleware.cors import CORSMiddleware
from database.otp_accessor import Otp_Accessor
from database.users_accsesor import User_Accessor
from login import LoginRouter,LoginService
from database.models.base import Base
from dotenv import load_dotenv

from otp_router import Opt_service, Otp_router

            
auth_handler = AuthHandler()

def protected(username=Depends(auth_handler.auth_wrapper)):
    return {"status": "ok", "username": username}

def create_startup(app):
    async def startup():
        """
          @brief this function starts the server.
        """
        #sql-------#

        engine = create_engine("sqlite:///database.db")
        Session = sessionmaker(bind=engine)
        session = Session()
        Base.metadata.create_all(engine)
        #----Login----#
        login_acceessor = Admin_Accessor(session,admins)
        l_service = LoginService(login_acceessor)
        app.include_router(LoginRouter(name="users",service=l_service,auth_handler=auth_handler),prefix="/login")
        #----USERS--#
        users_accessor = User_Accessor(session,Users)
        #----OTP----#
        otp_accessor = Otp_Accessor(session,OTP_Session)
        otp_service = Opt_service(otp_accessor,users_accessor=users_accessor)
        app.include_router(Otp_router(name="otp",service=otp_service),prefix="/otp")

        app.add_api_route("/protected",endpoint=protected,methods=["GET"])

    return startup

def main():
    load_dotenv()
    print(os.getenv("SUPER_SECRET_SALT"))
    app = FastAPI()
    origins = [ "*" ]
    app.add_event_handler("startup",create_startup(app))
    # to allow js programs to accsess the server
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    #start the server
    run(app, host="0.0.0.0", port=8090)

if "__main__" == __name__:
    main()
