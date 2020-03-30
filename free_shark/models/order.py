from free_shark.db import get_db,abort
import time


class Order:
    def __init__(self,**kwargs):
        self._id=kwargs.get('id',None)
        self._commodity_id=kwargs.get('commodity_id',None)
        self._commodity_name=kwargs.get('commodity_name',None)
        self._buyer_id=kwargs.get('buyer_id',None)
        self._school_number=kwargs.get('school_number',None)
        self._status=kwargs.get('status',None)
        self._create_time=kwargs.get('create_time',None)
        print("到这里了！！！！！！！！！")
    
    @staticmethod
    def add_order(**kwargs):
        orde=Order(**kwargs) 
        db = get_db()
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 创建时间
        create_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print(create_time)
        sql = "INSERT INTO comorder(commodity_id,commodity_name,buyer_id,school_number,status,create_time) VALUES (%s,%s,%s,%s,%s,%s)"
        try:
            # 执行sql语句
            print("执行sql语句")
            cursor.execute(sql,(orde._commodity_id,orde._commodity_name,orde._buyer_id,orde._school_number,orde._status,create_time))
            # 提交到数据库执行
            print("提交到数据库执行")
            db.commit()
            return 1
        except Exception as e:
            # 如果发生错误则回滚
            db.rollback()
            print(e)
            raise e
        # 关闭数据库连接
        db.close()
    
    def delete_order(self):
        db = get_db()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        print(self._id)
        sql = "DELETE FROM comorder WHERE id = %s"
        try:
            # 执行sql语句
            cursor.execute(sql,(self._id))
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()
            # 关闭数据库连接
        db.close()

    @staticmethod
    def create_ord_from_rows(row):
        orde=Order(id=row[0],commodity_id=row[1],commodity_name=row[2],buyer_id=row[3],school_number=row[4],status=row[5],create_time=row[6])
        return orde

    @staticmethod
    def get_order_by_id(id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT* FROM comorder WHERE id = %s',str(id))
        results = cursor.fetchone()
        print("results=",results)
        if results is None:
            return None
        orde=Order.create_ord_from_rows(results)
        return orde
        db.close()

    @staticmethod
    def get_order_by_school_number(school_number):
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT* FROM comorder WHERE school_number = %s or buyer_id=%s',(str(school_number),str(school_number)))
        results = cursor.fetchall()
        print(results)
        ordes=[]
        if results is None:
            return None
        for result in results:
            orde=Order.create_ord_from_rows(result)
            ordes.append(orde)
        return ordes,len(ordes)
        db.close()

    @staticmethod
    def get_order_by_buyer_id(buyer_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT* FROM comorder WHERE buyer_id = %s',str(buyer_id))
        results = cursor.fetchone()
        print("results=",results)
        if results is None:
            return None
        orde=Order.create_ord_from_rows(results)
        return orde
        db.close()

    @staticmethod
    def get_order_by_commodity_id(commodity_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT* FROM comorder WHERE commodity_id = %s',(str(commodity_id)))
        results = cursor.fetchone()
        if results is None:
            return None
        orde=Order.create_ord_from_rows(results)
        return orde
        db.close()

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self,new_val):
        self._status=new_val
        db = get_db()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        # 创建时间
        sql = "UPDATE comorder SET status=%s WHERE id=%s"
        try:
            # 执行sql语句
            cursor.execute(sql,(self._status,self._id))
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()
            raise
            # 关闭数据库连接
        db.close() 

    #查看作为卖家没有处理的订单
    @staticmethod
    def get_order_by_school_number_and_status(school_number,new_value):
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT* FROM comorder WHERE school_number = %s and status = %s',(str(school_number),(str(new_value))))
        results = cursor.fetchall()
        print("results=",results)
        ordes=[]
        if results is None:
            return None
        for result in results:
            orde=Order.create_ord_from_rows(result)
            ordes.append(orde)
        return ordes,len(ordes)
        db.close()

    
    @staticmethod
    def search_user_without_page(id="%%",commodity_id="%%",commodity_name="%%",buyer_id="%%",school_number="%%",status="%%",create_time="%%"):
        sql="""
        SELECT * FROM comorder WHERE 
            id LIKE %s AND
            commodity_id LIKE %s AND 
            commodity_name LIKE %s AND 
            buyer_id LIKE %s AND
            school_number LIKE %s AND
            status LIKE %s AND
            create_time LIKE %s
            """
        db = get_db()
        cursor=db.cursor()
        cursor.execute(sql,(id,commodity_id,commodity_name,buyer_id,school_number,status,create_time))
        print(id,commodity_id,commodity_name,buyer_id,school_number,status,create_time)
        print(cursor.mogrify(sql,(id,commodity_id,commodity_name,buyer_id,school_number,status,create_time)))
        results=cursor.fetchall()
        ordes=[]
        if results is None:
            return None
        for result in results:
            orde=Order.create_ord_from_rows(result)
            ordes.append(orde)
        return ordes,len(ordes)
        db.close()

    @staticmethod
    def get_order_by_id_commodity(id=None,commodity_name=None,school_number=None):
        db = get_db()
        cursor = db.cursor()
        if commodity_name is None and id is None:
            cursor.execute('SELECT* FROM comorder WHERE school_number = %s or buyer_id=%s',(str(school_number),str(school_number)))
        elif commodity_name is None:
            cursor.execute('SELECT* FROM comorder WHERE id = %s and (school_number = %s or buyer_id=%s)',(str(id),str(school_number),str(school_number)))
        elif id is None:
            cursor.execute('SELECT* FROM comorder WHERE commodity_name = %s and (school_number = %s or buyer_id=%s)',(str(commodity_name),str(school_number),str(school_number)))
        else:
            cursor.execute('SELECT* FROM comorder WHERE (id = %s or commodity_name = %s) and (school_number = %s or buyer_id=%s)',(str(id),str(commodity_name),str(school_number),str(school_number)))
        results = cursor.fetchall()
        print(results)
        ordes=[]
        if results is None:
            return None
        for result in results:
            orde=Order.create_ord_from_rows(result)
            ordes.append(orde)
        return ordes,len(ordes)
        db.close()
