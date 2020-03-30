from tests import app,client

def test_username_available_case1(client):
    rv=client.post("/api/user/check_username",data={
        "username":"test1"
    })
    assert rv.get_json()['status'] != 200

def test_username_available_case2(client):
    rv=client.post("/api/user/check_username",data={
        "username":"fcc"
    })
    assert rv.get_json()['status'] == 200

def test_email_available_case1(client):
    rv=client.post("/api/user/check_email",data={
        "email":"email"
    })
    assert rv.get_json()['status']!=200

def test_email_available_case2(client):
    rv=client.post("/api/user/check_email",data={
        "email":"email@email.com"
    })
    assert rv.get_json()['status']==200