from abc import ABC, abstractmethod
from datetime import datetime


class User(ABC):

   def __init__(self , username , user_id,password, role_id , last_login ,last_logout,status = "ACTIVE" , created_at = datetime.now()):

    self.username = username
    self.user_id=user_id
    self.password=password
    self.role_id = role_id
    self.status=status
    self.careated_at=datetime.now()
    self.last_login= last_login#how to make the datetime in the login/out cases
    self.last_logout=last_logout

    def login(self):

        self.last_login= datetime.now()
        print(f"The user {self.username} last logged in at {self.last_login.strftime('%Y-%m-%d %H:%M:%S')}")


    def logout(self):

        self.last_logout= datetime.now()
        print(f"The user {self.username} last logged out at {self.last_logout.strftime('%Y-%m-%d %H:%M:%S')}")



    #2 ways for menu either main or user class as abstract





