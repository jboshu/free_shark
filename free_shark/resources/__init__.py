from free_shark.resources.blue_print import bp
from flask_restful import Api, Resource
from free_shark.resources.user_resource import user_resource,user_register_resource
from free_shark.resources import block_resource 
from free_shark.resources.statistics_resource import block_stat_resource
from free_shark.resources.statistics_resource import user_stat_resource
from free_shark.resources.configs import errors

api=Api(bp,errors=errors)
api.add_resource(user_resource.UserResourceAdd,'/user/add')
api.add_resource(user_resource.UserResourceSearch,'/user/search')
api.add_resource(user_resource.UserResourceDelete,'/user/delete')
api.add_resource(user_resource.UserResourceUpdate,'/user/update')
api.add_resource(user_register_resource.UsernameAvailable,'/user/check_username')
api.add_resource(user_register_resource.EmailAvailable,'/user/check_email')
api.add_resource(user_register_resource.SendActivationEmail,'/user/send_act_email')
api.add_resource(user_resource.UserRecoverResource,'/user/redoDelete')

api.add_resource(block_resource.BlockSearchResource,'/block/search')
api.add_resource(block_resource.QuickBlockResource,'/block/quickCreate')
api.add_resource(block_resource.BlockAddResource,'/block/add')
api.add_resource(block_resource.BlockDeleteResource,'/block/delete')

api.add_resource(block_stat_resource.BlockDuringStatResource,'/stat/block/during')
api.add_resource(block_stat_resource.BlockStartStatResource,'/stat/block/start')
api.add_resource(block_stat_resource.BlockEndStatResource,'/stat/block/end')
api.add_resource(user_stat_resource.UserRegisterStatResource,'/stat/user/register')

@bp.route("/heartbeat",methods=["GET","POST"])
def heartbeat():
    return "ok"
