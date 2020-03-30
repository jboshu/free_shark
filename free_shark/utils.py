from functools import wraps
from flask import request,current_app
from flask_login import current_user,login_required
from flask_principal import Permission,RoleNeed
import hmac
from hashlib import sha512
import os

def admin_login_required(func):
    @wraps(func)
    @login_required
    def decorated_view(*args,**kwargs):
        permission=Permission(RoleNeed("admin"))
        if not permission.can():
            return current_app.login_manager.unauthorized()
        else:
            return func(*args,**kwargs)
    return decorated_view

from flask_restful import fields
class Arg_Default_Val(fields.Raw):
    def __init__(self,default_class=str,default_val=None):
        self.default_val=default_val
        self.default_class=default_class
    
    def __call__(self,value):
        if value is None:
            return self.default_class(self.default_val)
        else:
            return self.default_class(value)

def with_default_val(default_class=str,default_val=None):
    return Arg_Default_Val(default_class,default_val)

def drop_value_from_request(default=None):
    def formatter(func):
        @wraps(func)
        def decorated_view(self):
            d=self.parser.parse_args()
            for key in d:
                if d[key]==None:
                    self.parser.remove_argument(key)
            return func(self)
        return decorated_view
    return formatter

def make_secure_token(*args, **options):
    '''
    This will create a secure token that you can use as an authentication
    token for your users. It uses heavy-duty HMAC encryption to prevent people
    from guessing the information. (To make it even more effective, if you
    will never need to regenerate the token, you can  pass some random data
    as one of the arguments.)

    :param \*args: The data to include in the token.
    :type args: args
    :param \*\*options: To manually specify a secret key, pass ``key=THE_KEY``.
        Otherwise, the ``current_app`` secret key will be used.
    :type \*\*options: kwargs
    '''
    key = options.get('key').encode("utf8")

    l = [s if isinstance(s, bytes) else s.encode('utf-8') for s in args]

    payload = b'\0'.join(l)

    token_value = hmac.new(key, payload, sha512).hexdigest()

    if hasattr(token_value, 'decode'):  # pragma: no cover
        token_value = token_value.decode('utf-8')  # ensure bytes

    return token_value

def load_config_from_envvar():
    d={}
    db_host=os.environ.get("DB_HOST")

    if db_host:
        d['DB_HOST']=db_host
    db_user=os.environ.get("DB_USER")

    if db_user:
        d['DB_USER']=db_user
    
    db_password=os.environ.get("DB_PASSWORD")
    if db_password:
        d['DB_PASSWORD']=db_password
    
    db_port=os.environ.get("DB_PORT")
    if db_port:
        d['DB_PORT']=int(db_port)
    
    db_charset=os.environ.get("DB_CHARSET")
    if db_charset:
        d['DB_CHARSET']=db_charset
    
    database=os.environ.get("DATABASE")
    if database:
        d['DATABASE']=database
    
    return d

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

api_limiter=Limiter(key_func=get_remote_address,default_limits=["2000 per minute",])

from flask_mail import Mail
mail = Mail()

import re
def is_email(email):
    pattern=r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$"   #邮箱仅允许字母数字下划线和横杠
    return re.match(pattern,email)

def check_email(email):
    if is_email(email):
        return email
    else:
        raise ValueError("%s is not a email!" % email)

def replace_dict(d,target,value):
    d[target]=value
    return d

def set_default(d,key,value):
    d.setdefault(key,value)
    return d

from datetime import datetime
def date_parser(str):
    return datetime.strptime(str,"%Y-%m-%d %H:%M:%S")

