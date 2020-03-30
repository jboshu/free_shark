from tests import client,app
import pytest
import free_shark
from flask_login import current_user
from flask_login.mixins import AnonymousUserMixin
from free_shark.models.user import User

def login(client,username,password):
    rv=client.post("/auth/login",data={
        "username":username,
        "password":password
    },follow_redirects=True)
    assert bytes(username,encoding="utf8") in rv.data
    return rv,client

def logout(client):
    return client.get("/auth/logout",follow_redirects=True),client


@pytest.fixture
def admin_login(app):
    with app.test_client() as client:
        rv,client=login(client,"testAdmin","123456")
        yield client,app
        logout(client)

@pytest.fixture(params=[("test1","123456")])
def user_login(app,request):
    with app.test_client(request) as client:
        rv,client=login(client,request.param[0],request.param[1])
        yield client,app
        logout(client)

@pytest.mark.parametrize("username, password",[("test1","123456"),("test2","123456"),("testAdmin","123456")])
def test_login(client,username,password):
    rv,client=login(client,username,password)
    assert bytes(username,encoding="utf8") in rv.data


def test_logout(admin_login):
    client=admin_login[0]
    app=admin_login[1]
    rv=client.get("/auth/logout",follow_redirects=True)
    with app.app_context():
        assert current_user.is_anonymous


@pytest.mark.parametrize("username,password,email",[("ftt","xnpyxnpy","ftt@qq.com"),("fcc","fcc123","123456@gamil.com"),("sleep_gay","hxmwll","hxm@hxm.com")])
def test_add_user_api_case1(admin_login,username,password,email):
    client,app=admin_login
    rv=client.post("/api/user/add",data={
        "username":username,
        "password":password,
        "email":email
    })
    d=rv.get_json()
    assert d['status']==200
    with app.app_context():
        user=User.get_user_by_username(username)
        assert user.check_password(password)

@pytest.mark.parametrize("username",["test1","test2"])
def test_del_user_api_case1(admin_login,username):
    client,app=admin_login
    with app.app_context():
        id=User.get_user_by_username(username).id
    rv=client.post("/api/user/delete",data={
        "id":id
    })
    d=rv.get_json()
    assert d['status']==200
    with app.app_context():
        user=User.get_user_by_username(username)
        assert user is None

def test_del_user_api_case2(admin_login):
    client,app=admin_login
    with app.app_context():
        id=current_user.id
    rv=client.post("/api/user/delete",data={
        "id":id
    })
    code=rv.status_code
    assert code==401

@pytest.mark.parametrize("username",["test1","test2"])
def test_search_user_with_username_api_case1(admin_login,username):
    client,app=admin_login
    rv=client.post("/api/user/search",data={
        "username":username,
        "page_num":1,
        "page_size":20
    })
    d=rv.get_json()
    assert d['count']==1
    assert d['data'][0]['username']==username

@pytest.mark.parametrize("username,expect_count",[("test",3),("tes",3),("Admin",1)])
def test_search_user_with_username_api_case2(admin_login,username,expect_count):
    client,app=admin_login
    rv=client.post("/api/user/search",data={
        "username":"%"+username+"%",
        "page_num":1,
        "page_size":20
    })
    d=rv.get_json()
    assert d['count']==len(d['data']) and d['count']==expect_count
    for item in d['data']:
        assert username in item['username']

@pytest.mark.parametrize("email",["email","yyy@yyy.com"])
def test_search_user_with_email_api_case1(admin_login,email):
    client,app=admin_login
    rv=client.post("/api/user/search",data={
        "email":email,
        "page_num":1,
        "page_size":20
    })
    d=rv.get_json()
    print(d)
    assert d['count']==1
    assert d['data'][0]['email']==email

@pytest.mark.parametrize("id,username",[(1,"test11"),(2,"test22")])
def test_update_user_admin_case1(admin_login,id,username):
    client,app=admin_login
    rv=client.post("/api/user/update",data={
        "username":username,
        "id":id
    })
    d=rv.get_json()
    assert d['status']==200
    with app.app_context():
        user=User.get_user_by_id(id)
        assert user.username==username

@pytest.mark.parametrize("id,email",[(1,"test11@test.com"),(2,"test22@test.com")])
def test_update_user_admin_case2(admin_login,id,email):
    client,app=admin_login
    rv=client.post("/api/user/update",data={
        "email":email,
        "id":id
    })
    d=rv.get_json()
    assert d['status']==200
    with app.app_context():
        user=User.get_user_by_id(id)
        assert user.email==email

def test_update_user_noadmin_case1(user_login):
    client,app=user_login
    rv=client.post("/api/user/update",data={
        "email":"123@123.com",
        "id":3
    })
    d=rv.get_json()

    assert not "status" in d

def test_update_user_noadmin_case2(user_login):
    client,app=user_login
    email="123@123.com"
    with app.app_context():
        id=current_user.id
    rv=client.post("/api/user/update",data={
        "email":email,
        "id":id
    })
    d=rv.get_json()
    assert d['status']==200
    with app.app_context():
        assert current_user.email=="123@123.com"  
        user=User.get_user_by_id(id)
        assert user.email==email

@pytest.mark.parametrize("username,email",[("test2","ttt@ttt.com"),("tststs","rrr"),("test2","rrr")])
def test_update_user_case1(admin_login,username,email):
    client,app=admin_login
    with app.app_context():
        id=current_user.id
    rv=client.post("/api/user/update",data={
        "username":username,
        "email":email,
        "id":id
    })
    d=rv.get_json()
    print(rv.data.decode("utf8"))
    assert d['status']!=200
    with app.app_context():
        user=User.get_user_by_id(id)
        assert user.username!=username or user.email != email
