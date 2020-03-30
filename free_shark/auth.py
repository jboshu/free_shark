from flask import (Blueprint, flash, g, render_template,
                   request, session, redirect, url_for, render_template_string, current_app)
from werkzeug.security import check_password_hash,generate_password_hash
from werkzeug.exceptions import Forbidden
from free_shark.forms import login_form,student_form
from free_shark.models import user
from free_shark.models import student
from free_shark.models import order
from free_shark.models.commodity import Commodity
from flask_principal import identity_loaded,UserNeed,RoleNeed,identity_changed,Identity,AnonymousIdentity
from flask_login import login_user,login_required,logout_user,current_user
from free_shark.resources.user_resource.user_register_resource import SendActivationEmailPermission
from flask import abort
from flask_mail import Message
from free_shark.utils import mail

bp=Blueprint('auth',__name__,url_prefix='/auth')

@bp.route('/login',methods=("GET","POST"))
def login():
    form=login_form.LoginForm()
    if form.validate_on_submit():
        c_user=user.User.attempt_login(form.data['username'],form.data['password'])   #需要按需加载用户信息
        print("is blocked?",c_user.is_blocked)
        if c_user.is_blocked and c_user.is_authenticated():
                flash("你已被封禁, 最近的封禁记录: 因 %s 被封号至 %s " % (c_user.active_block_list[0].reason,c_user.active_block_list[0].end_time) ,"warning")
        elif c_user.is_authenticated():
            login_user(c_user,remember=form.data['remember'])  #需要加入next跳转
            if c_user.is_forbid:
                flash("你还没有激活账户,请快去<a href='/auth/send_activation'>激活</a>!","warning")
            if c_user.is_admin:
                flash("尊敬的管理员, 请前往<a href='/admin'>页面</a>管理系统!","success")
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(c_user.id))
            next = request.args.get('next')
            print(next)
            # next_is_valid should check if the user has valid
            # permission to access the `next` url
            flash("Hi %s!" % c_user.username,"success")
            return redirect(next or url_for('auth.login'))
            
            #return render_template_string("Hi {{ current_user.username }}!")   #需要修改模板
        else:
            flash("wrong password!","danger")
    return render_template("login.html",form=form)

@bp.route("/editUser")
def editUser():
    targets=request.args.get("target")
    usernameInputEnable=False
    passwordInputEnable=False
    emailInputEnable=False
    if targets is not None:
        targets=targets.split(",")
        if "username" in targets:
            usernameInputEnable=True
        if "password" in targets:
            passwordInputEnable=True
        if "email" in targets:
            emailInputEnable=True
    return render_template("edit_userinfo.html",
        usernameInputEnable=usernameInputEnable,
        passwordInputEnable=passwordInputEnable,
        emailInputEnable=emailInputEnable
        )

@bp.route("/register",methods=("GET",))
def register():
    if current_user.is_authenticated:
        logout()


    return render_template("register.html")

send_email_permission=SendActivationEmailPermission()


@bp.route("/send_activation")
@send_email_permission.require(403)
def send_activation():
    return render_template("send_activation_email.html")



@bp.route("/activation/<token>")
def activation(token):
    c_user=user.User.get_user_by_token(token)
    print(c_user)
    if c_user is None or not c_user.is_forbid:
        return redirect(url_for("auth.login"))
    else:
        login_user(c_user)  #需要加入next跳转
        c_user.status=1
        identity_changed.send(current_app._get_current_object(),
                                identity=Identity(c_user.id))
    return render_template("activation_success.html")


@bp.route('/test',methods=("GET","POST"))
def test():
    form=student_form.StudentForm()
    data ={}
    if form.validate_on_submit():
        print("form_data=",form.data)
        stu=student.Student.get_student_real_name(form.data['real_name'])
        stu.update_college=form.data['college']
        data = {
        "real_name": stu._real_name,
        "college": stu._college,
        "user_id": stu._user_id,
        "school_number": stu._school_number,
        "banji": stu._banji,
        "contact": stu._contact
        }
        #return "已更新！！！！！"
    return render_template("testStudent.html",form=form,data=data)

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    identity_changed.send(current_app._get_current_object(),
                        identity=AnonymousIdentity())
    return redirect(url_for("auth.login"))

@login_required
@bp.route('/indexorder',methods=("GET","POST"))
def indexorder():
    if request.method == 'GET':
        user_id = current_user.id
        print(user_id)
        if user_id is not None:
            stu=student.Student.get_student_id(user_id)
            print(stu._school_number)
            ordes,count=order.Order.get_order_by_school_number(stu._school_number)
            print(ordes)
            print(count)
            user_school_number=stu._school_number
            return render_template("comorder.html",ordes=ordes,user_school_number=user_school_number)
        elif user_id is None:
            return render_template("comorder.html")
        else:
            abort(404)
@login_required    
@bp.route('/searchorder',methods=("GET","POST"))
def searchorder():
    if request.method == 'GET':
        commodity_name = request.args.get('commodity_name') or None
        order_id = request.args.get('order_id') or None
        user_id = current_user.id
        print(commodity_name)
        print(order_id)
        print(user_id)
        stu=student.Student.get_student_id(user_id)
        print(stu._school_number)
        user_school_number=stu._school_number
        if commodity_name is None and order_id is None:
            ordes,count = order.Order.get_order_by_id_commodity(school_number=str(stu._school_number))
        elif commodity_name is None:
            ordes,count = order.Order.get_order_by_id_commodity(id=str(order_id),school_number=str(stu._school_number))
        elif order_id is None:
            ordes,count = order.Order.get_order_by_id_commodity(commodity_name=str(commodity_name),school_number=str(stu._school_number))
        else:
            ordes,count = order.Order.get_order_by_id_commodity(id=str(order_id),commodity_name=str(commodity_name),school_number=str(stu._school_number))
        #r = Commodity.search_commodity(-1,0,sys.maxsize,1,commodity_type,commodity_name)
        print(ordes)
        print(count)
        # 设置分页
        return render_template("comorder.html",ordes=ordes,user_school_number=user_school_number)

@login_required
@bp.route('/search_order_status',methods=("GET","POST"))
def search_order_status():
    if request.method == 'GET':
        user_id = current_user.id
        print(user_id)
        if user_id is not None:
            stu=student.Student.get_student_id(user_id)
            user_school_number=stu._school_number
            ordes,count=order.Order.get_order_by_school_number_and_status(stu._school_number,"0")
            print(ordes)
            print(count)
            print(stu._school_number)
            return render_template("comorder.html",ordes=ordes,user_school_number=user_school_number)
        elif user_id is None:
            return render_template("comorder.html")
        else:
            abort(404)

@login_required
@bp.route('/update',methods=("GET","POST"))
def update():
    if request.method == 'GET':
        id = request.args.get('id') or None
        user_id = current_user.id
        new_status = request.args.get('new_status') or None
        if id is not None and user_id is not None:
            print(id)
            print(new_status)
            stu=student.Student.get_student_id(user_id)
            orde=order.Order.get_order_by_id(id)
            status=orde.status=new_status
            buyer = student.Student.get_student_by_school_number(orde._buyer_id)
            print(buyer._user_id)
            user1=user.User.get_user_by_id(buyer._user_id)
            print(user1.email)
            print(status)
            c=Commodity.get_commodity_by_id(orde._commodity_id)
            msg = Message('闲鲨交易通知',recipients=[user1.email])
            if new_status=='1':
                orde_id=str(orde._id)
                contact=str(stu._contact)
                msg.html = render_template_string("<h1>卖家已经同意出售：您预约的%s号商品,卖家联系方式是%s<h1/>" % (orde_id,contact))
                c.status=2
                c.update_commodity()
            else:
                orde_id=str(orde._id)
                contact=str(stu._contact)
                msg.html = render_template_string("<h1>非常抱歉，卖家不同意出售您预约的%s号商品<h1/>" % (orde_id))
                c.status=0
                c.update_commodity()
            mail.send(msg)
            return render_template("comorder.html")
        else:
            abort(404)

@login_required
@bp.route('/delete_order',methods=("GET","POST"))
def delete_order():
    if request.method == 'GET':
        id = request.args.get('id') or None
        if id is not None:
            orde=order.Order.get_order_by_id(id)
            orde.delete_order()
            c=Commodity.get_commodity_by_id(orde._commodity_id)
            c.status=0
            c.update_commodity()
            return render_template("comorder.html")
        elif id is None:
            abort(404)