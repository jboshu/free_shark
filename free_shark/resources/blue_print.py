from flask import Blueprint
import free_shark.resources.user_resource

bp=Blueprint("api",__name__,url_prefix="/api")

