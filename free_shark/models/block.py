from free_shark.db import get_db,get_db_with_dict_cursor
from free_shark.models import user

class Block:
    def __init__(self,id,user_id,reason,start_time,end_time):
        self._id=id
        self._user_id=user_id
        self._reason=reason
        self._start_time=start_time
        self._end_time=end_time

    def __str__(self):
        return "Block #%d user %d from %s to %s beacuse of %s" %(self._id,self._user_id,self._start_time,self._end_time,self._reason)

    def __repr__(self):
        return "Block #%d user %d from %s to %s beacuse of %s" %(self._id,self._user_id,self._start_time,self._end_time,self._reason)

    def block_id_not_none(func):
        def wrapper(self,*args,**kwargs):
            assert self._id is not None
            return func(self,*args,**kwargs)
        return wrapper

    @property
    def is_active(self):
        from datetime import datetime
        if datetime.now()>self._start_time and datetime.now()<self._end_time:
            return True
        else:
            return False

    @property
    def id(self):
        return self._id
    
    @property
    def user_id(self):
        return self._user_id

    @property
    @block_id_not_none
    def user(self):
        c_user=user.User.get_user_by_id(self.user_id)
        return c_user

    @user_id.setter
    @block_id_not_none
    def user_id(self,new_val):
        db=get_db()
        cursor=db.cursor()
        sql="UPDATE block SET user_id=%s WHERE id=%s"
        try:
            cursor.execute(sql,(new_val,self.id))
            db.commit()
        except:
            db.rollback()
            raise
    
    @property
    def reason(self):
        return self._reason
    
    @reason.setter
    @block_id_not_none
    def reason(self,new_val):
        db=get_db()
        cursor=db.cursor()
        sql="UPDATE block SET reason=%s WHERE id=%s"
        try:
            cursor.execute(sql,(new_val,self.id))
            db.commit()
        except:
            db.rollback()
            raise

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    @block_id_not_none
    def start_time(self,new_val):
        db=get_db()
        cursor=db.cursor()
        sql="UPDTE block SET start_time=%s WHERE id=%s"
        try:
            cursor.execute(sql,(new_val,self.id))
            db.commit()
        except:
            db.rollback()
            raise


    @property
    def end_time(self):
        return self._end_time
    
    @end_time.setter
    @block_id_not_none
    def end_time(self,new_val):
        db=get_db()
        cursor=db.cursor()
        sql="UPDTE block SET end_time=%s WHERE id=%s"
        try:
            cursor.execute(sql,(new_val,self.id))
            db.commit()
        except:
            db.rollback()
            raise

    @block_id_not_none
    def del_block(self):
        db=get_db()
        cursor=db.cursor()
        sql="DELETE FROM block WHERE id=%s"
        try:
            cursor.execute(sql,self.id)
            db.commit()
        except:
            db.rollback()
            raise

    @staticmethod
    def get_block_list_by_user_id(user_id):
        db=get_db()
        cursor=db.cursor()
        sql="SELECT id,user_id,reason,start_time,end_time FROM block WHERE user_id=%s"
        try:
            cursor.execute(sql,user_id)
            results=cursor.fetchall()
            ans=[]
            for result in results:
                ans.append(Block(*result))
            return ans
        except:
            db.rollback()
            raise

    @staticmethod
    def get_block_by_id(id):
        db=get_db()
        cursor=db.cursor()
        sql="SELECT id,user_id,reason,start_time,end_time FROM block WHERE id=%s"
        try:
            cursor.execute(sql,id)
            result=cursor.fetchone()
            return Block(*result)
        except:
            db.rollback()
            raise

    @staticmethod
    def get_active_block_list_by_user_id(user_id):
        db=get_db()
        cursor=db.cursor()
        sql="""
        SELECT id,user_id,reason,start_time,end_time
        FROM block 
        WHERE user_id=%s 
        AND TIMEDIFF(start_time,CURRENT_TIMESTAMP())<0 
        AND TIMEDIFF(end_time,CURRENT_TIMESTAMP())>0
        """
        try:
            #print(cursor.mogrify(sql,str(user_id)))
            cursor.execute(sql,str(user_id))
            
            results=cursor.fetchall()
            ans=[]
            for result in results:
                ans.append(Block(*result))
            return ans
        except:
            db.rollback()
            raise
    
    @staticmethod
    def create_block(user_id,reason,start_time,end_time):
        db=get_db()
        cursor=db.cursor()
        sql="INSERT INTO block (user_id,reason,start_time,end_time) VALUES(%s,%s,%s,%s)"
        try:
            cursor.execute(sql,(user_id,reason,start_time,end_time))
            db.commit()
            sql="SELECT LAST_INSERT_ID();"
            cursor.execute(sql)
            result=cursor.fetchone()
            print(result)
            block=Block.get_block_by_id(result[0])
            print(block)
            return block
        except:
            db.rollback()
            raise

    @staticmethod
    def search(id="%%",user_id="%%",username="%%",reason="%%",page_num=1,page_size=20):
        db=get_db()
        cursor=db.cursor()
        sql="""
        SELECT block.id,block.user_id,block.reason,block.start_time,block.end_time
        FROM block 
        RIGHT JOIN user ON block.user_id=user.id 
        WHERE block.id LIKE %s AND 
        block.user_id LIKE %s AND
        user.username LIKE %s AND 
        block.reason LIKE %s
        """
        try:
            cursor.execute(sql,(id,user_id,username,reason))
            results=cursor.fetchall()
            ans=[]
            for block in results:
                ans.append(Block(*block))
            return ans[(page_num-1)*page_size:page_num*page_size],len(ans)
        except:
            db.rollback()
            raise