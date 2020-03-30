import datetime
from flask import abort,flash
from flask_restful import Resource,reqparse,fields,marshal_with
from flask_principal import Permission,RoleNeed,UserNeed
from free_shark.models.block import Block
from free_shark.models.user import User
from free_shark.resources.configs import Block_Search_Fields,Base_Response_Fields
from free_shark.utils import admin_login_required,date_parser,drop_value_from_request

class BlockSearchPermission(Permission):
    def __init__(self,user_id):
        super().__init__()
        self.needs=set([RoleNeed("admin"),RoleNeed(user_id)])



class BlockSearchResource(Resource):

    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("user_id",required=True,type=int)

    @marshal_with(Block_Search_Fields().resource_fields)
    def post(self):
        d=self.parser.parse_args()
        permission = BlockSearchPermission(d['user_id'])
        user=User.get_user_by_id(d['user_id'])
        if permission.can():
            blocks=user.block_list
            count=int(len(blocks))
            return Block_Search_Fields(user.username,blocks,count=count)
        else:
            abort(401)
    
class QuickBlockResource(Resource):
    def __init__(self):
        super().__init__()
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("user_id",required=True,type=int)
        self.parser.add_argument("reason",required=True)
        self.parser.add_argument("time",required=True,type=int)
    
    @admin_login_required
    @marshal_with(Base_Response_Fields().resource_fields)
    def post(self):
        d=self.parser.parse_args()
        start_time=datetime.datetime.now()-datetime.timedelta(seconds=5)
        end_time=start_time+datetime.timedelta(days=d['time'])
        try:
            block=Block.create_block(d['user_id'],d['reason'],start_time,end_time)
            print(block)
            flash("用户 %s 已因为%s封禁 %d 天!" % (block.user.username,d['reason'],d['time']),"warning")
        except:
            raise
        return Base_Response_Fields("ok")

class BlockAddResource(Resource):
    def __init__(self):
        super().__init__()
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("user_id",required=False,type=int)
        self.parser.add_argument("username",required=False)
        self.parser.add_argument("reason",required=True)
        self.parser.add_argument("start_time",required=True,type=date_parser)
        self.parser.add_argument("end_time",required=True,type=date_parser)

    @drop_value_from_request()
    @admin_login_required
    @marshal_with(Base_Response_Fields().resource_fields)
    def post(self):
        d=self.parser.parse_args()
        if d['end_time']<d['start_time']:
            abort(400)
        if "user_id" in d:
            user=User.get_user_by_id(d['user_id'])
        elif "username" in d:
            user=User.get_user_by_username(d['username'])
            if user is None:
                abort(404)
        else:
            abort(400)
        block=Block.create_block(user.id,d['reason'],d['start_time'],d['end_time'])
        print(block)
        flash("用户 %s 已因为%s 从 %s 被封禁到 %s" % (block.user.username,d['reason'],d['start_time'],d['end_time']),"warning")
        return Base_Response_Fields("ok")

class BlockDeleteResource(Resource):
    def __init__(self):
        super().__init__()
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("id",required=True,type=int)
    
    @admin_login_required
    @marshal_with(Base_Response_Fields().resource_fields)
    def post(self):
        d=self.parser.parse_args()
        block=Block.get_block_by_id(d['id'])
        if block is None:
            abort(404)
        else:
            try:
                block.del_block()
                flash("成功移除了记录!","danger")
                return Base_Response_Fields("ok")
            except:
                abort(500)
                raise
        