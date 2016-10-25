#coding=utf-8
from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.http import HttpRequest
from django.test import TestCase
from django.test import Client
from datetime import datetime
from unittest import mock

from sign.views import index
from django.contrib.auth.models import User
from sign.models import Event, Guest
import time


# Create your tests here.
class IndexPageTest(TestCase):
    ''' 测试index登录首页'''

    def test_root_url_resolves_to_index_page(self):
        ''' 测试根url是否解析到登录页 '''
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_index_page_returns_correct_html(self):
        ''' 测试调用index函数返回的页与模板加载的index2.html是否相等 '''
        request = HttpRequest()
        response = index(request)
        expected_html = render_to_string('index.html')
        self.assertEqual(response.content.decode(), expected_html)


class LoginActionTest(TestCase):
    ''' 测试登录动作'''

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')

    def test_add_author_email(self):
        ''' 测试添加用户 '''
        user = User.objects.get(username="admin")
        self.assertEqual(user.username, "admin")
        self.assertEqual(user.email, "admin@mail.com")

    def test_login_action_username_password_null(self):
        ''' 用户名密码为空 '''
        c = Client()
        response = c.post('/login_action/', {'username':'','password':''})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password null!", response.content)

    def test_login_action_username_password_error(self):
        ''' 用户名密码错误 '''
        c = Client()
        response = c.post('/login_action/', {'username':'abc','password':'123'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)

    def test_login_action_success(self):
        ''' 登录成功 '''
        c = Client()
        response = c.post('/login_action/', data = {'username':'admin','password':'admin123456'})
        self.assertEqual(response.status_code, 302)


class EventMangeTest(TestCase):
    ''' 发布会管理 '''

    def setUp(self):
        Event.objects.create(name="xiaomi5",limit=2000,address='beijing',status=1,start_time='2017-8-10 12:30:00')

    def test_add_event_data(self):
        ''' 测试添加发布会 '''
        event = Event.objects.get(name="xiaomi5")
        self.assertEqual(event.address, "beijing")

    def test_event_mange_success(self):
        ''' 测试发布会:xiaomi5 '''
        c = Client()
        response = c.post('/event_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"xiaomi5", response.content)
        self.assertIn(b"beijing", response.content)

    def test_event_mange_sreach_success(self):
        ''' 测试发布会搜索 '''
        c = Client()
        response = c.post('/sreach_name/',{"name":"xiaomi5"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"xiaomi5", response.content)
        self.assertIn(b"beijing", response.content)


class GuestManageTest(TestCase):
    ''' 嘉宾管理 '''

    def setUp(self):
        Event.objects.create(id=1,name="xiaomi5",limit=2000,address='beijing',status=1,start_time='2017-8-10 12:30:00')
        Guest.objects.create(realname="alen",phone=18611001100,email='alen@mail.com',sign=0,event_id=1)

    def test_add_guest_data(self):
        ''' 测试添加嘉宾 '''
        guest = Guest.objects.get(realname="alen")
        self.assertEqual(guest.phone, "18611001100")
        self.assertEqual(guest.email, "alen@mail.com")
        self.assertFalse(guest.sign)

    def test_event_mange_success(self):
        ''' 测试嘉宾信息: alen '''
        c = Client()
        response = c.post('/guest_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"alen", response.content)
        self.assertIn(b"18611001100", response.content)

    def test_guest_mange_sreach_success(self):
        ''' 测试嘉宾搜索 '''
        c = Client()
        response = c.post('/sreach_phone/',{"phone":"18611001100"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"alen", response.content)
        self.assertIn(b"18611001100", response.content)


class SignIndexActionTest(TestCase):
    ''' 发布会签到 '''

    def setUp(self):
        Event.objects.create(id=1,name="xiaomi5",limit=2000,address='beijing',status=1,start_time='2017-8-10 12:30:00')
        Event.objects.create(id=2,name="oneplus4",limit=2000,address='shenzhen',status=1,start_time='2017-6-10 12:30:00')
        Guest.objects.create(realname="alen",phone=18611001100,email='alen@mail.com',sign=0,event_id=1)
        Guest.objects.create(realname="una",phone=18611001101,email='una@mail.com',sign=1,event_id=2)

    def test_sign_index_action_phone_null(self):
        ''' 手机号为空 '''
        c = Client()
        response = c.post('/sign_index_action/1/',{"phone":""})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"phone error.", response.content)

    def test_sign_index_action_phone_or_event_id_error(self):
        ''' 手机号或发布会id错误 '''
        c = Client()
        response = c.post('/sign_index_action/2/',{"phone":"18611001100"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"event id or phone error.", response.content)

    def test_sign_index_action_user_sign_has(self):
        ''' 用户已签到 '''
        c = Client()
        response = c.post('/sign_index_action/2/',{"phone":"18611001101"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"user has sign in.", response.content)

    def test_sign_index_action_sign_success(self):
        ''' 签到成功 '''
        c = Client()
        response = c.post('/sign_index_action/1/',{"phone":"18611001100"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"sign in success!", response.content)


'''
运行所有用例：
python3 manage.py test

运行sign应用下的所有用例：
python3 manage.py test sign

运行sign应用下的tests.py文件用例：
python3 manage.py test sign.tests

运行sign应用下的tests.py文件中的 GuestManageTest 测试类：
python3 manage.py test sign.tests.GuestManageTest

......


'''