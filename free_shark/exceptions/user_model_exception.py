from werkzeug.exceptions import HTTPException
class UserModelException(HTTPException):
    def __init__(self,**kwargs):
        super(UserModelException,self).__init__(**kwargs)


class UserEmailInvalid(UserModelException):
    def __init__(self,wrong_email):
        super(UserEmailInvalid,self).__init__(description="Incorrect email.")
        self.wrong_email=wrong_email
        


class UsernameDuplicate(UserModelException):
    def __init__(self,wrong_username):
        super(UsernameDuplicate,self).__init__(description="Username is used.")
        self.wrong_username=wrong_username


class UserNotFound(UserModelException):
    def __init__(self,wrong_key,wrong_id):
        super(UserModelException,self).__init__(description="Username is used.")
        self.wrong_key=wrong_key
        self.wrong_id=wrong_id