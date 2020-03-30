from flask import Blueprint,render_template,flash,current_app,request,abort
from flask.views import MethodView
from free_shark.utils import admin_login_required
from free_shark.models.user import User
from free_shark.models.block import Block

bp=Blueprint('admin',__name__,url_prefix='/admin')


class AdminView(MethodView):

    default_page_num=1
    default_page_size=20

    def get_target(self):
        raise NotImplementedError()

    def get_template_name(self):
        raise NotImplementedError()

    def render_template(self,**context):
        return render_template(self.get_template_name(),**context)

    @admin_login_required
    def get(self):
        d=request.args.to_dict()
        d.setdefault('page_size',self.default_page_size)
        d.setdefault('page_num',self.default_page_num)
        d['page_size']=int(d['page_size'])
        d['page_num']=int(d['page_num'])
        method=request.args.get("method")
        target=self.get_target()
        page_num=self.default_page_num
        page_size=self.default_page_size
        if request.args.get("page_num"):
            page_num=int(request.args.get("page_num"))
        if request.args.get("page_size"):
            page_size=int(request.args.get("page_size"))
        if not method:
            ans,count=target.search(page_size=page_size,page_num=page_num)
            print(ans)
            return self.render_template(ans=ans,count=count,page_num=page_num,page_size=page_size)
        elif method=='search':
            del d['method']
            ans,count=target.search(**d)
            flash("为您搜索到%d条记录" % count,"success")
            return self.render_template(ans=ans,count=count,page_num=page_num,page_size=page_size)
        else:
            abort(404)

class UserAdminView(AdminView):

    def get_template_name(self):
        return "admin/user.html"

    def get_target(self):
        return User


class BlockAdminView(AdminView):

    def get_template_name(self):
        return "admin/block.html"

    def get_target(self):
        return Block

class IndexView(MethodView):
    def get(self):
        return render_template("admin/index.html")

bp.add_url_rule('/user',view_func=UserAdminView.as_view("admin_user_view"))
bp.add_url_rule('/block',view_func=BlockAdminView.as_view("admin_block_view"))
bp.add_url_rule('/',view_func=IndexView.as_view("index_view"))