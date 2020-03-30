from flask import abort,current_app,url_for,render_template_string
from flask_mail import Message
from flask_login import current_user
from flask_restful import Resource,reqparse,fields,marshal_with
from flask_principal import Permission,RoleNeed,UserNeed
from free_shark.models.user import User
from free_shark.resources.configs import Base_Response_Fields,USER_EMAIL_INVALID,USERNAME_DUPLICATE
from free_shark.utils import api_limiter
from free_shark.utils import mail,check_email

class UserRegisterPermission(Permission):
    def __init__(self):
        super().__init__()
        self.excludes=set(RoleNeed("user"))   #不允许已登录用户注册


class SendActivationEmailPermission(UserRegisterPermission):
    def __init__(self):
        super().__init__()
        self.needs.add(RoleNeed("forbid"))  #仅向未认证用户发送邮件


user_register_permission=UserRegisterPermission()
send_activation_email_permission=SendActivationEmailPermission()


class UsernameAvailable(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("username",required=True)
        self.parser.add_argument("id",required=False)

    @marshal_with(Base_Response_Fields().resource_fields)
    def post(self):
        d=self.parser.parse_args()
        user=User.get_user_by_username(d['username'])
        if user is None:
            return Base_Response_Fields("ok")
        elif d.get("id",None) is not None:
            id=d.get("id")
            n_user=User.get_user_by_id(id)
            if n_user.username==d.get("username"):
                return Base_Response_Fields("ok")        
        else:
            return Base_Response_Fields("该用户名已被注册!",USERNAME_DUPLICATE)

class EmailAvailable(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("email",required=True)
        self.parser.add_argument("id",required=False)
    
    @marshal_with(Base_Response_Fields().resource_fields)
    def post(self):
        d=self.parser.parse_args()
        users=User.search_user_without_page(email=d['email'])
        if len(users)==0:
            return Base_Response_Fields("ok")
        elif d.get("id",None) is not None:
            id=d.get("id")
            n_user=User.get_user_by_id(id)
            if n_user.email==d.get("email"):
                return Base_Response_Fields("ok")
        else:
            return Base_Response_Fields("该邮箱已被注册!",USER_EMAIL_INVALID)

class SendActivationEmail(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("email",required=True,type=check_email)
    
    @marshal_with(Base_Response_Fields().resource_fields)
    @api_limiter.limit("5 per miniute")
    @send_activation_email_permission.require()
    def post(self):
        d=self.parser.parse_args()
        token=current_user.get_auth_token()
        url="http://localhost:5000"+url_for("auth.activation",token=token)
        msg=Message(
            token,
            recipients=[d['email']],
            )
        msg.subject="激活确认邮件"
        msg.html=render_template_string("<a href='{{url}}'>点此激活</a>",url=url)
        try:
            mail.send(msg)
            return Base_Response_Fields("success")
        except:
            return Base_Response_Fields("fail",500)

    def get(self):
        return self.post()