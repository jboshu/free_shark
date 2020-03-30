import sys
import os
sys.path.append(os.path.abspath('.'))
import pytest
from free_shark.models.order import Order
import free_shark
from flask import Flask
from free_shark.exceptions.user_model_exception import UserEmailInvalid
from tests import app



class TestOrder:
    #@pytest.mark.parametrize('id',[1])
    def test_add_stu1(self,app):
        with app.app_context():
            Order.add_order(commodity_id='1',commodity_name='上好佳',buyer_id='2',school_number='2016141225117',status='1')
            orde=Order.get_order_by_id(3)
            assert orde is not None

    def test_select_by_id(self,app):
        with app.app_context():
            orde=Order.get_order_by_id(251)
            assert orde is None

    @pytest.mark.parametrize('value',['35','36'])
    def test_select1_by_commodity_id(self,app,value):
        with app.app_context():
            orde=Order.get_order_by_commodity_id(value)
            assert orde is not None

    def test_select2_by_commodity_id(self,app):
        with app.app_context():
            orde=Order.get_order_by_commodity_id(7)
            assert orde is None

    def test_user_delete1(self,app):
        with app.app_context():
            Order.add_order(commodity_id='1',commodity_name='背背佳',buyer_id='5',school_number='6',status='2')
            orde=Order.get_order_by_id(5)
            assert orde is not None
            orde.delete_order()
            orde=Order.get_order_by_id(5)
            assert orde is None

    def test_update_status(self,app):
        with app.app_context():
            orde=Order.get_order_by_id(3)
            orde.status='0'
            assert orde.status=='0'

    @pytest.mark.parametrize('value',['2016141225117','2016141225117'])
    def test_select1_by_school_number_and_status0(self,app,value):
        with app.app_context():
            orde=Order.get_order_by_school_number_and_status(value,"0")
            assert orde is not None

    def test_select1_by_school_number(self,app):
        with app.app_context():
            ordes,count=Order.get_order_by_school_number(2016141225117)
            assert len(ordes)==count
            assert ordes[0]._id==1 and ordes[1]._id==4 and ordes[2]._id==5

    def test_select1_by_buyer_id(self,app):
        with app.app_context():
            orde=Order.get_order_by_buyer_id(2016141241188)
            assert orde is not None

    def test_select_search_user(self,app):
        with app.app_context():
            temp = 35
            ordes,count=Order.search_user_without_page(commodity_id="%"+str(temp)+"%")
            assert len(ordes)==count
            assert ordes[0]._id==1
