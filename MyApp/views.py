# -*- coding: utf-8 -*-
import logging
from httplib import HTTPResponse

from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import make_password
from models import *
from forms import *

# 输出日志信息
logger = logging.getLogger('MyApp.views')


def index(request):
    return render(request, 'index.html', locals())


# 注册
def doRegister(request):
    try:
        if request.method == 'POST':
            registerForm = RegisterForm(request.POST)
            # 注册
            if registerForm.is_valid():
                user = User.objects.create(
                    username=registerForm.cleaned_data["username"],
                    email=registerForm.cleaned_data["email"],
                    password=make_password(registerForm.cleaned_data["password"]),
                )
                user.save()

                # 登录
                user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认的登录验证方式
                login(request, user)
                return redirect('index')
        else:
            registerForm = RegisterForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'register.html', locals())


# 登陆
def doLogin(request):
    try:
        if request.method == 'POST':
            loginForm = LoginForm(request.POST)
            if loginForm.is_valid():
                # 登录
                username = loginForm.cleaned_data["username"]
                password = loginForm.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认的登录验证方式
                    login(request, user)
                else:
                    return render(request, 'login.html', {
                        "loginForm": loginForm,
                        "loginFailed": "账户或密码错误",
                    })
                return redirect('index')
        else:
            loginForm = LoginForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'login.html', locals())


def addModel(request):
    try:
        if request.method == 'POST':
            uploadForm = UploadForm(request.POST, request.FILES)
            if uploadForm.is_valid():
                bundle = Bundle.objects.create(id_user=request.user if request.user.is_authenticated() else None,
                                               name=uploadForm.cleaned_data["modelName"],
                                               # config_info=,
                                               # QRcode=,
                                               model=uploadForm.cleaned_data["model"],
                                               imageTarget=uploadForm.cleaned_data["imageTarget"],
                                               note=uploadForm.cleaned_data["note"],
                                               )
                bundle.save()
        else:
            uploadForm = UploadForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'add-model.html', locals())

def model(request):
    return render(request, 'models.html', locals())
