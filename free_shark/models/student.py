from free_shark.db import get_db,abort
import time


class Student:
    def __init__(self,**kwargs):
        self._user_id=kwargs.get('user_id',None)
        self._school_number=kwargs.get('school_number',None)
        self._real_name=kwargs.get('real_name',None)
        self._college=kwargs.get('college',None)
        self._banji=kwargs.get('banji',None)
        self._contact=kwargs.get('contact',None)
        self._create_time=kwargs.get('create_time',None)
        print("到这里了！！！！！！！！！")
    
    @staticmethod
    def add_student(**kwargs):
        stu=Student(**kwargs) 
        db = get_db()
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 创建时间
        create_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print(create_time)
        sql = "INSERT INTO student(user_id,school_number,real_name,college,banji,contact,create_time) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        try:
            # 执行sql语句
            print("执行sql语句")
            cursor.execute(sql,(stu._user_id,stu._school_number,stu._real_name,stu._college,stu._banji,stu._contact,create_time))
            # 提交到数据库执行
            print("提交到数据库执行")
            db.commit()
        except Exception as e:
            # 如果发生错误则回滚
            db.rollback()
            raise e
        # 关闭数据库连接
        db.close()
    
    def delete_student(self):
        db = get_db()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        sql = "DELETE FROM student WHERE user_id = %s"
        try:
            # 执行sql语句
            cursor.execute(sql,(self._user_id))
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()
            # 关闭数据库连接
        db.close()

    @staticmethod
    def create_stu_from_rows(row):
        stu=Student(user_id=row[1],school_number=row[2],real_name=row[3],college=row[4],banji=row[5],contact=row[6],create_time=row[7])
        return stu

    @staticmethod
    def get_student_id(user_id):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute('SELECT* FROM student WHERE user_id = %s',str(user_id))
            results = cursor.fetchone()
            if results is None:
                return None
            stu=Student.create_stu_from_rows(results)
        except Exception as e:
            print ("Error: unable to fetch data")
            print (e)
            raise e
        return stu
        db.close()

    @staticmethod
    def get_student_real_name(real_name):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute('SELECT* FROM student WHERE real_name = %s',str(real_name))
            results = cursor.fetchone()
            if results is None:
                return None
            stu=Student.create_stu_from_rows(results)
        except Exception as e:
            print ("Error: unable to fetch data")
            print (e)
            raise e
        return stu
        db.close()

    @staticmethod
    def get_student_by_school_number(school_number):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute('SELECT* FROM student WHERE school_number = %s',str(school_number))
            results = cursor.fetchone()
            if results is None:
                return None
            stu=Student.create_stu_from_rows(results)
        except Exception as e:
            print ("Error: unable to fetch data")
            print (e)
            raise e
        return stu
        db.close()

    @property
    def update_college(self):
        return self._college

    @update_college.setter
    def update_college(self,new_val):
        self._college=new_val
        db = get_db()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        # 创建时间
        sql = "UPDATE student SET college=%s WHERE user_id=%s"
        try:
            # 执行sql语句
            cursor.execute(sql,(self._college,self._user_id))
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()
            # 关闭数据库连接
        db.close() 

    @property
    def update_banji(self):
        return self._banji

    @update_banji.setter
    def update_banji(self,new_val):
        self._banji=new_val
        db = get_db()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        # 创建时间
        sql = "UPDATE student SET banji=%s WHERE user_id=%s"
        try:
            # 执行sql语句
            cursor.execute(sql,(self._banji,self._user_id))
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()
            # 关闭数据库连接
        db.close() 

    @property
    def update_contact(self):
        return self._contact

    @update_contact.setter
    def update_contact(self,new_val):
        self._contact=new_val
        db = get_db()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        # 创建时间
        sql = "UPDATE student SET contact=%s WHERE user_id=%s"
        try:
            # 执行sql语句
            cursor.execute(sql,(self._contact,self._user_id))
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()
            # 关闭数据库连接
        db.close()    