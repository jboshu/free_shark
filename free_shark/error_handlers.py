from flask import render_template,flash,redirect,url_for

def frobidden_handler(e):
    flash("权限不足,请登录或返回!")
    return redirect(url_for("auth.login"))