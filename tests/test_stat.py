from tests import app,client
from tests.test_userAPI import admin_login

def test_block_stat_start(admin_login):
    client,app=admin_login
    rv=client.get("/api/stat/block/start",data={
        "start_time":"2019-1-1 1:1:1",
        "end_time":"2019-12-31 23:59:59"
    })
    print(rv.get_json())
    assert rv.get_json()['data']

def test_block_stat_end(admin_login):
    client,app=admin_login
    rv=client.get("/api/stat/block/end",data={
        "start_time":"2019-1-1 1:1:1",
        "end_time":"2019-12-31 23:59:59"
    })
    print(rv.get_json())
    assert rv.get_json()['data']

def test_block_stat_during(admin_login):
    client,app=admin_login
    rv=client.get("/api/stat/block/end",data={
        "start_time":"2019-1-1 1:1:1",
        "end_time":"2019-12-31 23:59:59"
    })
    print(rv.get_json())
    assert rv.get_json()['data']

def test_user_stat(admin_login):
    client,app=admin_login
    rv=client.get("/api/stat/user/register",data={
        "start_time":"2019-1-1 1:1:1",
        "end_time":"2019-12-31 23:59:59"
    })
    print(rv.get_json())
    assert rv.get_json()['data']