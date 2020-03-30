import sys
import os
sys.path.append(os.path.abspath('.'))
import pytest
from free_shark.models.user import User
from tests import app
import free_shark
from flask import Flask
from free_shark.exceptions.user_model_exception import UserEmailInvalid




class TestUser:

    def test_add_user1(self,app):
        with app.app_context():
            user=User.create_user(username='zjm',password='kxxh',salt='kxxh',email='test@test',activation='act',type=2,status=2)
            assert user is not None
            user=User.get_user_by_username('zjm')
            assert user is not None
            assert user.salt=="kxxh"

    def test_get_user_by_username(self,app):
        with app.app_context():
            user=User.get_user_by_username("test1")
            assert user is not None

    def test_select2(self,app):
        with app.app_context():
            user=User.get_user_by_id(251)
            assert user is None

    def test_select1(self,app):
        with app.app_context():
            user=User.get_user_by_id(2)
            assert user is not None

    def test_modify_username1(self,app):
        with app.app_context():
            user=User.get_user_by_id(1)
            user.username='fcc'
            user=User.get_user_by_id(1)
            assert user.username=='fcc'

    def test_modify_password(self,app):
        with app.app_context():
            user=User.get_user_by_id(1)
            user.password='passwd'
            user=User.get_user_by_id(1)
            assert user.check_password('passwd')


    def test_modify_salt(self,app):
        with app.app_context():
            user=User.get_user_by_id(1)
            user.salt='passwd'
            user=User.get_user_by_id(1)
            assert user.salt=='passwd'   

    def test_modify_activation(self,app):
        with app.app_context():
            user=User.get_user_by_id(1)
            user.activation='test_act'
            user=User.get_user_by_id(1)
            assert user.activation=='test_act'   

    def test_modify_email_right_case(self,app):
        with app.app_context():
            user=User.get_user_by_id(1)
            user.email='test@test.com'
            user=User.get_user_by_id(1)
            assert user.email=='test@test.com'     

    def test_modify_email_wrong_case(self,app):
        with app.app_context():
            user=User.get_user_by_id(1)
            with pytest.raises(UserEmailInvalid):
                user.email='test_email' #此处应该抛出异常
    
    def test_modify_type(self,app):
        with app.app_context():
            user=User.get_user_by_id(1)
            user.type=3
            user=User.get_user_by_id(1)
            assert user.type==3

    def test_modify_status(self,app):
        with app.app_context():
            user=User.get_user_by_id(1)
            user.status=0
            user=User.get_user_by_id(1)
            assert user.status==0

    def test_user_delete1(self,app):
        with app.app_context():
            user=User.get_user_by_username("test2")
            assert user is not None
            user.delete_user()

    def test_user_login_success_case(self,app):
        with app.app_context():
            user=User.attempt_login("test1","123456")
            assert user.username=='test1'
            assert user.is_authenticated() is True
    
    def test_user_login_fail_case(self,app):
        with app.app_context():
            user=User.attempt_login("test1","123")
            assert user.is_authenticated() is False
    
    def test_user_query1(self,app):
        with app.app_context():
            users,count=User.search_user(username="test1")
            assert len(users)==count
            assert users[0].username=="test1"

    def test_user_query2(self,app):
        with app.app_context():
            users,count=User.search_user(username="%test%")
            assert len(users)==count
            assert users[0].username=="test1" and users[1].username=="test2"

    def test_user_token_generate(self,app):
        with app.app_context():
            user=User.get_user_by_id(1)
            assert user.get_auth_token() is not None