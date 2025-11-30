#!/usr/bin/python
# _*_ coding: utf-8 _*_
# @Time    : 2025/10/27 13:05
# @Author  : Seven
# @File    : urls.py
# @Software: PyCharm
from django.urls import path, include, re_path
from .views import RegisterView, UsernameCountView, MobileCountView, LoginView, LogoutView, UserInfoView, EmailView, \
    VerifyEmailView, AddressView, CreateAddressView, UpdateDestroyAddressView, DefaultAddressView, \
    UpdateTitleAddressView, ChangePasswordView
from meiduo_mall.utils.converters import UsernameConverter, MobileConverter

app_name = 'users'

urlpatterns = [
    # 用户诸恶
    path('register/', RegisterView.as_view(), name='register'),
    # re_path(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', UsernameCountView.as_view(), name='username'),
    # 判断用户名是否重复注册
    path('usernames/<username:username>/count/', UsernameCountView.as_view(), name='username'),
    # 判断手机号是否重复注册
    path('mobiles/<mobile:mobile>/count/', MobileCountView.as_view(), name='mobile'),
    # 用户登录
    path('login/', LoginView.as_view(), name='login'),
    # 用户退出
    path('logout/', LogoutView.as_view(), name='logout'),
    # 用户中心
    path('info/', UserInfoView.as_view(), name='info'),
    # 添加邮箱
    path('emails/', EmailView.as_view(), name='email'),
    path('emails/verification/', VerifyEmailView.as_view()),
    # 用户地址
    path('addresses/', AddressView.as_view(), name='address'),
    # 新增用户地址
    path('addresses/create/', CreateAddressView.as_view()),
    # 更新和删除地址
    re_path(r'addresses/(?P<address_id>\d+)/$', UpdateDestroyAddressView.as_view()),
    # 设置默认地址
    re_path(r'addresses/(?P<address_id>\d+)/default/$', DefaultAddressView.as_view()),
    # 更新title
    re_path(r'addresses/(?P<address_id>\d+)/title/$', UpdateTitleAddressView.as_view()),
    # 修改密码
    path('pass/', ChangePasswordView.as_view(), name='pass'),
]
