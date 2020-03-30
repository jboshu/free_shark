from free_shark.db import get_db, get_db_with_dict_cursor
import time
class Comment:
    def __init__(self,**kwargs):
        self._id = kwargs.get('id',None)
        self._comment_content = kwargs.get('comment_content', '')
        self._commodity_id = kwargs.get('commodity_id', None)
        self._user_id = kwargs.get('user_id',None)
        self._username = kwargs.get('username','')
        self._status = kwargs.get('status',0)
        self._create_time = kwargs.get('create_time', None)

    @property
    def id(self):
        return self._id

    @property
    def comment_content(self):
        return self._comment_content

    @comment_content.setter
    def comment_content(self, new_comment_content):
        self._comment_content = new_comment_content

    @property
    def commodity_id(self):
        return self._commodity_id

    @commodity_id.setter
    def commodity_id(self, new_commodity_id):
        self._commodity_id = new_commodity_id

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, new_user_id):
        self._user_id = new_user_id

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, new_username):
        self._username = new_username

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status):
        self._status = new_status

    @property
    def create_time(self):
        return self._create_time

    @create_time.setter
    def create_time(self, new_create_time):
        self._create_time = new_create_time

    # 增加评论 用户调用
    def add_comment(self):
        self._create_time = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        success = 0
        sql = "insert into comment(comment_content,commodity_id,user_id,username,status,create_time) \
            VALUES('%s',%d,%d,'%s',%d,'%s')" % (
                self._comment_content,
                self._commodity_id,
                self._user_id,
                self._username,
                self._status,
                self._create_time
            )

        try:
            db = get_db()
            cursor = db.cursor()
            print(sql)
            cursor.execute(sql)
            db.commit()
            success = 1
        except:
            db.rollback()
        
        db.close()
        return success

    # 删除评论 管理员调用 需要改为修改状态
    def delete_comment_by_id(id):
        success = 0
        sql = "delete from comment where id = %d" % (id)

        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
            success = 1
        except:
            db.rollback()

        db.close()
        return success

    # 得到某个商品的最新的五条评论 根据时间排序
    def get_comment_by_commodity_id(commodity_id):
        sql = "select * from comment where commodity_id = %d and status = 0 \
            order by create_time desc limit 0,5" % (commodity_id)
        
        results = []
        db = get_db_with_dict_cursor()
        cursor = db.cursor()
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            time = row['create_time']
            row['create_time'] = time.strftime(
            '%Y-%m-%d %H:%M:%S')
            comment = Comment(**row)
            results.append(comment)
        db.close()
        return results
            
