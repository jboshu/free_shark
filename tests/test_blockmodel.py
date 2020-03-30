from tests import app,client
from free_shark.models.block import Block

def test_block_add(app):
    with app.app_context():
        block=Block.create_block(1,"无可奉告","2019-01-01 1:1:1","2019-02-02 2:2:2")
        assert block is not None
        assert block.user_id==1
        assert block.is_active==False
    
def test_block_search(app):
    with app.app_context():
        block=Block.create_block(1,"无可奉告","2019-01-01 1:1:1","2019-02-02 2:2:2")
        block=Block.get_block_list_by_user_id(1)
        assert isinstance(block,list)
        assert block[0].user_id==1

def test_block_getter(app):
    with app.app_context():
        block=Block.create_block(1,"无可奉告","2019-01-01 1:1:1","2019-02-02 2:2:2")
        print(block)
        str(block)
        assert block.id
        assert block.reason
        assert block.start_time
        assert block.end_time
        assert block.user_id
        assert block.user.username=="test1"