from flask import current_app
from flask_login import UserMixin,current_user

from werkzeug.security import check_password_hash, generate_password_hash
import re
from free_shark.db import get_db,close_db,db_required,abort,get_db_with_dict_cursor
from free_shark.exceptions.db_exception import DB_Exception
from free_shark.exceptions.user_model_exception import UserModelException,UserEmailInvalid,UsernameDuplicate
from free_shark.utils import make_secure_token
from free_shark.models.block import Block
from free_shark.db import get_db,close_db,db_required,abort

class User(UserMixin):

    def __init__(self,**kwargs):
        super().__init__()
        self._id=kwargs.get('id',None)
        self._username=kwargs.get('username',None)
        self._password=kwargs.get('password',"")
        self._salt=kwargs.get('salt',"salt")
        self._email=kwargs.get('email',None)
        self._activation=kwargs.get('activation','act')
        self._type=kwargs.get('type',1)
        self._status=kwargs.get('status',2)
        self._create_time=kwargs.get('create_time',None)
        self._token=kwargs.get('token',None)
        self._activite_flag=False
        self._block_list=None
        self._active_block_list=None
    
    def __repr__(self):
        return ("Type: User. username: %s, role: %s" % (self.username,self.role))

    def is_authenticated(self):
        return self._activite_flag

    def get_id(self):
        return str(self._id)

    def get_auth_token(self):
        if self._token is None:
            db=get_db()
            cursor=db.cursor()
            sql="""
            SELECT token FROM token WHERE user_id=%s 
            """
            try:
                cursor.execute(sql,self.id)
                result=cursor.fetchone()
            except:
                db.rollback()
                abort(500)
            if result is None:
                self._token=make_secure_token(str(self._id),self._password,self._salt,key=current_app.config['SECRET_KEY'])
                sql="""
                INSERT INTO token (user_id,token) VALUES(%s,%s)
                """
                try:
                    cursor.execute(sql,(self.id,self._token))
                    db.commit()
                except:
                    db.rollback()
                    abort(500)
            else:
                self._token=result[0]
        return self._token

    def user_id_not_none(func):
        def wrapper(self,*args,**kwargs):
            if self.id is None:
                print('User id should not None!')
                abort(500)
            else:
                func(self,*args,**kwargs)
        return wrapper

    def login(self):
        self._activite_flag=True

    def recover(self):
        if self.status<0:
            self.status=-self.status

    @property
    def role(self):
        ans=[]
        if self.is_deleted:
            ans.append("deleted")
        if self.is_blocked:
            ans.append("blocked")
            #return ans
        if self.is_forbid:
            ans.append("forbid")
            #return ans
        if self.type==1:
            ans.append("user")
        elif self.type==0:
            ans.append("admin")
        return ans

    @property
    def id(self):
        return self._id

    @property
    def is_user(self):
        return self.type==1

    @property
    def is_deleted(self):
        return self.status<0

    @property
    def is_admin(self):
        return self.type==0

    @property
    def is_forbid(self):
        if self.is_admin:
            return False
        return self.status==2

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self,new_val):
        if self._username==new_val:
            return
        user=User.get_user_by_username(new_val)
        if user is not None:
            raise UsernameDuplicate(new_val)
        self._username=new_val
        db=get_db()
        cursor=db.cursor()
        try:
            cursor.execute("UPDATE user SET username=%s WHERE id=%s",(self._username,self._id))
            db.commit()
        except:
            db.rollback()
            abort(500)
        
    
    @property
    def password(self):
        return None
    
    def check_password(self,password):
        return check_password_hash(self._password,password)

    @password.setter
    def password(self,new_val):
        if self.check_password(new_val):
            return
        self._password=generate_password_hash(new_val)
        db=get_db()
        cursor=db.cursor()
        try:
            cursor.execute("UPDATE user SET password=%s WHERE id=%s",(self._password,self._id))
            db.commit()
        except:
            db.rollback()
            abort(500)
        

    @property
    def salt(self):
        return self._salt

    @salt.setter
    def salt(self,new_val):
        if self._salt==new_val:
            return
        self._salt=new_val
        db=get_db()
        cursor=db.cursor()
        try:
            cursor.execute("UPDATE user SET salt=%s WHERE id=%s",(self._salt,self._id))
            db.commit()
        except:
            db.rollback()
            abort(500)
        

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self,new_val):
        # 如果新值等于原始值则跳过修改
        from free_shark.utils import is_email
        if self._email==new_val:
            return
        if not is_email(new_val):
            raise UserEmailInvalid(new_val)
        self._email=new_val
        db=get_db()
        cursor=db.cursor()
        try:
            cursor.execute("UPDATE user SET email=%s WHERE id=%s",(self._email,self._id))
            db.commit()
            self.status=2
        except:
            db.rollback()
            abort(500)
        


    @property
    def activation(self):
        return self._activation
    
    @activation.setter
    def activation(self,new_val):
        # 如果新值等于原始值则跳过修改
        if self._activation==new_val:
            return
        self._activation=new_val
        db=get_db()
        cursor=db.cursor()
        try:
            cursor.execute("UPDATE user SET activation=%s WHERE id=%s",(self._activation,self._id))
            db.commit()
        except:
            db.rollback()
            abort(500)
        


    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self,new_val):
        # 如果新值等于原始值则跳过修改
        if self._type==new_val:
            return
        self._type=new_val
        db=get_db()
        cursor=db.cursor()
        try:
            cursor.execute("UPDATE user SET type=%s WHERE id=%s",(self._type,self._id))
            db.commit()
        except:
            db.rollback()
            abort(500)
        

    @property
    def status(self):
        return self._status
    
    @status.setter
    @user_id_not_none
    def status(self,new_val):
        # 如果新值等于原始值则跳过修改
        if self._status==new_val:
            return
        self._status=new_val
        db=get_db()
        cursor=db.cursor()
        try:
            cursor.execute("UPDATE user SET status=%s WHERE id=%s",(self._status,self._id))
            db.commit()
        except:
            db.rollback()
            abort(500)

    @property
    def create_time(self):
        return self._create_time
    
    @user_id_not_none
    def delete_user(self):
        db=get_db()
        cursor=db.cursor()
        try:
            cursor.execute("DELETE FROM user WHERE id=%s",self._id)
            db.commit()
        except:
            db.rollback()
            abort(500)
        
    @user_id_not_none
    def safe_delete_user(self):
        self.status=-self.status

    
    @property
    def is_blocked(self):
        if len(self.active_block_list):
            print("block:",self.active_block_list)
            return True
        else:
            return False
            
    @property
    def block_list(self):
        self._block_list=Block.get_block_list_by_user_id(self.id)
        return self._block_list

    @property
    def active_block_list(self):
        self._active_block_list=Block.get_active_block_list_by_user_id(self.id)
        return self._active_block_list


    def set_forbid(self,value):
        if value:
            self.status=2
        else:
            self.status=1

    @staticmethod
    def create_user_from_rows(row):
        user=User(id=row[0],username=row[1],password=row[2],salt=row[3],email=row[4],activation=row[5],type=row[6],status=row[7],create_time=row[8],token=row[9])
        return user

    @staticmethod
    def get_user_by_id(id,mask=0):
        db=get_db()
        cursor=db.cursor()
        cursor.execute('SELECT user.*,token.token FROM user LEFT JOIN token ON token.user_id=user.id WHERE user.id=%s AND user.status>=%s',(str(id),mask))
        result = cursor.fetchone()  #由于id的唯一性，至多只有一个结果
        if result is None:
            return None
        user=User.create_user_from_rows(result)
        cursor.close()
        
        return user

    @staticmethod
    def search_user(id="%%",username="%%",email="%%",activation="%%",type="%%",status="%%",create_time="%%",page_size=20,page_num=1,**kwargs):
        users=User.search_user_without_page(id,username,email,activation,type,status,create_time,**kwargs)
        return users[(page_num-1)*page_size:page_num*page_size],len(users)

    @staticmethod
    def search(*args,**kwargs):
        return User.search_user(*args,**kwargs)

    @staticmethod
    def search_user_without_page(id="%%",username="%%",email="%%",activation="%%",type="%%",status="%%",create_time="%%",mask=1):
        sql="""
        SELECT * FROM user WHERE 
            id LIKE %s AND
            username LIKE %s AND 
            email LIKE %s AND
            activation LIKE %s AND
            type LIKE %s AND
            status LIKE %s AND
            create_time LIKE %s 
            """
        if isinstance(mask,str):
            mask=int(mask)
        if mask>=0:
            sql+="AND status>=0"
        else:
            sql+="AND status<0"
        db=get_db_with_dict_cursor()
        cursor=db.cursor()
        cursor.execute(sql,(id,username,email,activation,type,status,create_time))
        print(cursor.mogrify(sql,(id,username,email,activation,type,status,create_time)))
        results=cursor.fetchall()
        users=[]
        for result in results:
            user=User(**result)
            users.append(user)
        return users

    @staticmethod
    def get_user_by_username(username,mask=0):
        db=get_db()
        cursor=db.cursor()
        cursor.execute('SELECT user.*,token.token FROM user LEFT JOIN token ON token.user_id=user.id WHERE user.username=%s AND user.status>=%s',(str(username),mask))
        #print(cursor.mogrify('SELECT user.*,token.token FROM user LEFT JOIN token ON token.user_id=user.id WHERE user.username=%s AND user.status>=%s',(str(username),mask)))
        result = cursor.fetchone()  #由于username的唯一性，至多只有一个结果
        if result is None:
            return None
        user=User.create_user_from_rows(result)
        cursor.close()
        
        return user

    @staticmethod
    def attempt_login(username,password):
        user = User.get_user_by_username(username)
        if user is None:
            return User()
        if user.check_password(password):
            user.login()
            return user
        else:
            return User()

    @staticmethod
    def create_user(**kwargs):
        assert 'username' in kwargs
        user=User.get_user_by_username(kwargs['username'])
        if user is not None:
            raise UsernameDuplicate(kwargs['username'])
        user=User(**kwargs)
        assert 'password' in kwargs
        user.password=kwargs['password']
        db=get_db()
        cursor=db.cursor()
        try:
            cursor.execute("INSERT INTO user (username,password,salt,email,activation,type,status,create_time) VALUES (%s,%s,%s,%s,%s,%s,%s,CURRENT_TIME())",(user.username,user._password,user.salt,user.email,user.activation,user.type,user.status))
            print(cursor.mogrify("INSERT INTO user (username,password,salt,email,activation,type,status,create_time) VALUES (%s,%s,%s,%s,%s,%s,%s,CURRENT_TIME())",(user.username,user._password,user.salt,user.email,user.activation,user.type,user.status)))
            
            db.commit()
            return User.get_user_by_username(user.username)
        except:
            db.rollback()
            abort(500)
        
    
    @staticmethod
    def get_user_by_token(token):
        db=get_db_with_dict_cursor()
        cursor=db.cursor()
        sql="""
        SELECT user.*,token.token FROM user LEFT JOIN token ON token.user_id=user.id WHERE token.token=%s AND user.status>=0
        """
        cursor.execute(sql,token)
        result=cursor.fetchone()
        if result is None:
            return None
        user=User(**result)
        return user
        

    @staticmethod
    def get_deleted_user_by_id(id):
        db=get_db_with_dict_cursor()
        cursor=db.cursor()
        sql="""
        SELECT user.*,token.token FROM user LEFT JOIN token ON token.user_id=user.id WHERE user.status<0 AND user.id=%s
        """
        cursor.execute(sql,id)
        result=cursor.fetchone()
        if result is None:
            return None
        user=User(**result)
        return user
