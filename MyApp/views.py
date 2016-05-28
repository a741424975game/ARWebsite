# -*- coding: utf-8 -*-
import logging
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import make_password
from MyApp.qrCode import generate_qrcode
from forms import *



# 输出日志信息
logger = logging.getLogger('MyApp.views')


def index(request):
    return render(request, 'index.html', locals())


# 注册
def do_register(request):
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
def do_login(request):
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


def add_model(request):
    try:
        if request.method == 'POST':
            uploadForm = UploadForm(request.POST, request.FILES)
            if uploadForm.is_valid():
                bundle = Bundle.objects.create(id_user=request.user if request.user.is_authenticated() else None,
                                               name=uploadForm.cleaned_data["modelName"],
                                               model=uploadForm.cleaned_data["model"],
                                               imageTarget=uploadForm.cleaned_data["imageTarget"],
                                               note=uploadForm.cleaned_data["note"],
                                               )
                bundle.save()
                api = settings.SITE_URL + 'arConfigInfo-api?bundle_id=' + str(bundle.id)
                generate_qrcode(api, str(bundle.QRCode)[8:])
        else:
            uploadForm = UploadForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'add-model.html', locals())


def models(request):
    try:
        models_list = User.objects.get(
            username=request.user if request.user.is_authenticated() else None
        ).bundle_set.all()
    except Exception as e:
        logger(e)
    return render(request, 'models.html', locals())


def view_model(request):
    return render(request, 'view-model.html', locals())


def my_account(request):
    return render(request, 'my-account.html', locals())


def edit_profile(request):
    return render(request, 'edit-profile.html', locals())


def help_page(request):
    return render(request, 'help.html', locals())


def ar_config_info_api(request):
    try:
        bundle_id = request.GET.get('bundle_id')
        if bundle_id is not None and Bundle.objects.filter(id=bundle_id):
            bundle = Bundle.objects.get(id=bundle_id)
            config_info = bundle.config_info
            return HttpResponse(config_info)
    except Exception as e:
        logger(e)
    return HttpResponse('error')

