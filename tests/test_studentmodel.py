import sys
import os
sys.path.append(os.path.abspath('.'))
import pytest
from free_shark.models.student import Student
import free_shark
from flask import Flask
from free_shark.exceptions.user_model_exception import UserEmailInvalid
from tests import app



class TestStudent:

    #@pytest.mark.parametrize('id',[1])
    def test_add_stu1(self,app):
        with app.app_context():
            Student.add_student(user_id='1',school_number='1111',real_name='五五开',college='ART',banji='1',contact='110')
            stu=Student.get_student_id(1)
            assert stu is not None

    def test_select1_id(self,app):
        with app.app_context():
            stu=Student.get_student_id(251)
            assert stu is None

    @pytest.mark.parametrize('value',['胡书杰','王超'])
    def test_select2_real_name(self,app,value):
        with app.app_context():
            stu=Student.get_student_real_name(value)
            assert stu is not None

    def test_select3_real_name(self,app):
        with app.app_context():
            stu=Student.get_student_real_name('金咕咕')
            assert stu is None

    def test_user_delete1(self,app):
        with app.app_context():
            Student.add_student(user_id='2',school_number='2312',real_name='PDD',college='CS',banji='1',contact='120')
            stu=Student.get_student_id(2)
            assert stu is not None
            stu.delete_student()

    def test_modify_college(self,app):
        with app.app_context():
            stu=Student.get_student_id(1)
            stu.update_college='AABB'
            stu=Student.get_student_id(1)
            assert stu.update_college=='AABB'   
    
    def test_modify_banji1(self,app):
        with app.app_context():
            stu=Student.get_student_id(1)
            stu.update_banji=6
            stu=Student.get_student_id(1)
            assert stu.update_banji=='6'

    def test_modify_contact(self,app):
        with app.app_context():
            stu=Student.get_student_id(2)
            stu.update_contact='13890254777'
            stu=Student.get_student_id(2)
            assert stu.update_contact=='13890254777'     
    