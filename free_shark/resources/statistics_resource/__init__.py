from flask_restful import Resource,reqparse,fields, marshal_with,marshal
from free_shark.utils import date_parser,admin_login_required

class StatResource(Resource):
    def __init__(self):
        super().__init__()
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("start_time",required=True,type=date_parser)
        self.parser.add_argument("end_time",required=True,type=date_parser)
    
    def get_stat_obj(self):
        raise NotImplementedError

    def get_result_fields(self):
        raise NotImplementedError

    @admin_login_required
    def get(self):
        d=self.parser.parse_args()
        results=self.get_stat_obj()(d['start_time'],d['end_time']).stat()
        fields=self.get_result_fields()
        return marshal(fields(results),fields().resource_fields)