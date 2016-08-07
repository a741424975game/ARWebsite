# -*- coding: utf-8 -*-
import logging
import requests
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.template import RequestContext
from forms import *

from MyApp.qrCode import generate_qrcode
from MyApp.handle import *
from MyApp.echarts import *
from MyApp.psutil_getServerInfo import *

# 输出日志信息
logger = logging.getLogger('MyApp.views')


# 需要将所有数据库操作整理

def home(request):
    return render(request, 'home.html', locals())


def index(request):
    try:
        if not request.user.is_authenticated():
            return redirect('login.html')
        daily_visits = 0
        monthly_visits = 0
        total_visits = 0
        comments_amount = 0
        likes = 0
        comments_list = []
        recently_months_visits = MonthlyVisits(request.user.username)
        region_rank = RegionRank(request.user.username)
        bundle_positive_rank = {}
        for bundle in User.objects.get(username=request.user.username).bundle_set.all():
            likes += bundle.likes
            scan_statistics = bundle.scanstatistics_set.all()
            comments_statistics = bundle.commentstatistics_set.all()
            comments_list += bundle.comment_set.all()
            comments_list.sort(key=lambda comment: comment.datetime, reverse=True)
            for each_statistics in scan_statistics:
                if each_statistics.datetime.month == timezone.localtime(timezone.now()).month:
                    monthly_visits += each_statistics.amount
                    if each_statistics.datetime.day == timezone.localtime(timezone.now()).day:
                        daily_visits += each_statistics.amount
                total_visits += each_statistics.amount
            for each_statistics in comments_statistics:
                comments_amount += each_statistics.amount
            comments = bundle.comment_set.all()
            positive = 0
            for each_comment in comments:
                if each_comment.sentiment >= 0.55:
                    positive += 1
            if bundle.comments != 0:
                bundle_positive_rank[bundle.id] = float(positive) / float(bundle.comments)
            else:
                bundle_positive_rank[bundle.id] = 0.0
        bundle_positive_rank = sorted(bundle_positive_rank.iteritems(), key=lambda p: p[1], reverse=True)
        temp = bundle_positive_rank
        bundle_positive_rank = []
        for each in temp:
            bundle_positive_rank.append((Bundle.objects.get(id=each[0]), each[1]))
    except Exception as e:
        logger.error(e)
    return render(request, 'index.html', locals())


# 注册
def do_register(request):
    try:
        if request.user.is_authenticated():
            return redirect('index.html')
        elif request.method == 'POST':
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
        if request.user.is_authenticated():
            return redirect('index.html')
        elif request.method == 'POST':
            loginForm = LoginForm(request.POST)
            if loginForm.is_valid():
                # 登录
                username = loginForm.cleaned_data["username"]
                password = loginForm.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认的登录验证方式
                    login(request, user)
                    return redirect('index.html')
            else:
                return render(request, 'login.html', {
                    "loginForm": loginForm,
                    "loginFailed": "账户或密码错误",
                })
        else:
            loginForm = LoginForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'login.html', locals())


# 注销
def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        logger.error(e)
    return redirect('login.html')


# 添加模型
def add_model(request):
    try:
        if request.user.is_authenticated():
            if request.method == 'POST':
                uploadForm = UploadForm(request.POST, request.FILES)
                if uploadForm.is_valid():
                    bundle = Bundle.objects.create(id_user=request.user,
                                                   name=uploadForm.cleaned_data["modelName"],
                                                   model=uploadForm.cleaned_data["model"],
                                                   imageTarget=uploadForm.cleaned_data["imageTarget"],
                                                   note=uploadForm.cleaned_data["note"],
                                                   product_link=uploadForm.cleaned_data["productLink"]
                                                   )
                    api = api_url_maker(str(bundle.id))  # 自定义的方法
                    generate_qrcode(api, str(bundle.QRCode)[8:])  # 去除路径只保留文件名
                    if bundle.imageTarget.name is None:
                        bundle.imageTarget = bundle.QRCode
                    config_info_json_data = ar_config_info_handle(bundle)
                    bundle.config_info = config_info_json_data
                    bundle.save()
                    return redirect('view-model.html?bundle_id=' + str(bundle.id))
            else:
                uploadForm = UploadForm()
        else:
            return redirect('login.html')
    except Exception as e:
        logger.error(e)
    return render(request, 'add-model.html', locals())


# 删除模型
def delete_model(request):
    try:
        if request.user.is_authenticated():
            bundle_id = request.GET.get('bundle_id')
            bundles_id = request.GET.getlist('bundles_id')
            if bundle_id is not None and Bundle.objects.filter(id=bundle_id):  # 需要整理
                model = Bundle.objects.get(id=bundle_id)
                model.model.delete(save=True)
                model.QRCode.delete(save=True)
                model.imageTarget.delete(save=True)
                model.delete()
            elif bundles_id is not None:
                for bundle_id in bundles_id:
                    if bundle_id is not None and Bundle.objects.filter(id=bundle_id):  # 需要整理
                        model = Bundle.objects.get(id=bundle_id)
                        model.model.delete(save=True)
                        model.QRCode.delete(save=True)
                        model.imageTarget.delete(save=True)
                        model.delete()
            else:
                return redirect('login.html')
    except Exception as e:
        logger.error(e)
    return redirect('models.html')


# 展示模型列表
def models(request):
    try:
        if request.user.is_authenticated():
            models_list = User.objects.get(
                username=request.user
            ).bundle_set.all()
        else:
            return redirect('login.html')
    except Exception as e:
        logger.error(e)
    return render(request, 'models.html', locals())


# 展示模型详细信息和数据
def view_model(request):
    try:
        if request.user.is_authenticated():
            bundle_id = request.GET.get('bundle_id')
            if bundle_id is not None and Bundle.objects.filter(id=bundle_id):
                model = Bundle.objects.get(id=bundle_id)
                comments_list = model.comment_set.all().order_by('-datetime')
                tags = model.keywordsstatistics_set.all().order_by('-amount')
                qrCodePath = model.QRCode.url
                imageTargetPath = model.imageTarget.url
                dailyVC = DailyVC(bundle_id)
                monthlyVC = MonthlyVC(bundle_id)
                areaVisits = AreaVisits(bundle_id)
            else:
                return redirect('404.html')
        else:
            return redirect('login.html')
    except Exception as e:
        logger.error(e)
    return render(request, 'view-model.html', locals())


# 用户账户
def my_account(request):
    return render(request, 'my-account.html', locals())


# 编辑账户
def edit_profile(request):
    return render(request, 'edit-profile.html', locals())


#  下载页面
def download(request):
    return render(request, 'download.html', locals())


# 帮助页面
def help_page(request):
    return render(request, 'help.html', locals())


# AR模型api
def ar_config_info_api(request):
    try:
        bundle_id = request.GET.get('bundle_id')
        ip = request.META['REMOTE_ADDR']
        is_ar_scanner = request.GET.get('is_ar_scanner')
        if is_ar_scanner is not None:
            if ip is not None and bundle_id is not None and Bundle.objects.filter(id=bundle_id):
                url = 'http://ip.taobao.com/service/getIpInfo.php?ip=' + ip
                response = requests.get(url)
                data = location_handle(response.json())
                if not Locations.objects.filter(province=data['data']['region'], city=data['data']['city'],
                                                county=data['data']['county'], ):
                    location = Locations.objects.create(province=data['data']['region'],
                                                        city=data['data']['city'],
                                                        county=data['data']['county'],
                                                        )
                    location.save()
                else:
                    location = Locations.objects.get(province=data['data']['region'],
                                                     city=data['data']['city'],
                                                     county=data['data']['county'],
                                                     )
                bundle = Bundle.objects.get(id=bundle_id)
                scan_id = Scan.objects.create(id_bundle=bundle, id_location=location).id
                config_info = json.loads(bundle.config_info)
                config_info['scanId'] = scan_id
                config_info_json = json.dumps(config_info)
                return HttpResponse(config_info_json)
        else:
            return render(request, 'download.html', locals())
    except Exception as e:
        logger.error(e)
    return HttpResponse('error')


# 评论api
def ar_comment_api(request):
    try:
        bundle_id = request.GET.get('bundle_id')
        scan_id = request.GET.get('scan_id')
        comment = request.GET.get('comment')
        ip = request.META['REMOTE_ADDR']
        if ip is not None and comment is not None and bundle_id is not None and scan_id is not None:
            if Bundle.objects.filter(id=bundle_id):
                url = 'http://ip.taobao.com/service/getIpInfo.php?ip=' + ip
                response = requests.get(url)
                data = location_handle(response.json())
                location = Locations.objects.get(province=data['data']['region'],
                                                 city=data['data']['city'],
                                                 county=data['data']['county'],
                                                 )
                bundle = Bundle.objects.get(id=bundle_id)
                comment_db = Comment.objects.create(id_bundle=bundle, id_location=location, content=comment)
                if ScanOperatingRecord.objects.filter(id_scan=Scan.objects.get(id=scan_id)):
                    scan_operating_record = ScanOperatingRecord.objects.get(id_scan=Scan.objects.get(id=scan_id))
                    if scan_operating_record.commented == 0.0:
                        scan_operating_record.commented = comment_db.sentiment
                else:
                    scan_operating_record = ScanOperatingRecord.objects.create(id_scan=Scan.objects.get(id=scan_id))
                    scan_operating_record.commented = comment_db.sentiment
                scan_operating_record.save()
            else:
                return HttpResponse('error')
        else:
            return HttpResponse('error')
    except Exception as e:
        logger.error(e)
        return HttpResponse('error')
    return HttpResponse('success')


# 获取评论api
def get_ar_comment_api(request):
    try:
        bundle_id = request.GET.get('bundle_id')
        page = request.GET.get('page')
        if page is not None and bundle_id is not None and Bundle.objects.filter(id=bundle_id):
            comments = Bundle.objects.get(id=bundle_id).comment_set.all()
            comments = Paginator(comments, 50)
            comments = comments.page(page)
            temp = []
            for comment in comments.object_list:
                temp.append(comment.content)
            comments = json.dumps(temp)
        else:
            return HttpResponse('error')
    except Exception as e:
        logger.error(e)
        return HttpResponse('error')
    return HttpResponse(comments)


# 商品链接被点击
def product_link_clicked_api(request):
    try:
        scan_id = request.GET.get('scan_id')
        if scan_id is not None:
            if ScanOperatingRecord.objects.filter(id_scan=Scan.objects.get(id=scan_id)):
                scan_operating_record = ScanOperatingRecord.objects.get(id_scan=Scan.objects.get(id=scan_id))
                if scan_operating_record.product_link_clicked == 0:
                    scan_operating_record.product_link_clicked = 1
            else:
                scan_operating_record = ScanOperatingRecord.objects.create(id_scan=Scan.objects.get(id=scan_id))
                scan_operating_record.product_link_clicked = 1;
            scan_operating_record.save()

        else:
            return HttpResponse('error')
    except Exception as e:
        logger.error(e)
        return HttpResponse('error')
    return HttpResponse('success')


# 点赞api
def ar_like_api(request):
    try:
        bundle_id = request.GET.get('bundle_id')
        scan_id = request.GET.get('scan_id')
        like = request.GET.get('like')
        if bundle_id is not None and scan_id is not None and Bundle.objects.filter(id=bundle_id):
            if like == '1':
                bundle = Bundle.objects.get(id=bundle_id)
                bundle.likes += 1
                bundle.save()
                if ScanOperatingRecord.objects.filter(id_scan=Scan.objects.get(id=scan_id)):
                    scan_operating_record = ScanOperatingRecord.objects.get(id_scan=Scan.objects.get(id=scan_id))
                    if scan_operating_record.liked == 0:
                        scan_operating_record.liked = 1;
                else:
                    scan_operating_record = ScanOperatingRecord.objects.create(id_scan=Scan.objects.get(id=scan_id))
                    scan_operating_record.liked = 1;
                scan_operating_record.save()
            else:
                bundle = Bundle.objects.get(id=bundle_id)
                bundle.likes -= 1
                bundle.save()
                if ScanOperatingRecord.objects.filter(id_scan=Scan.objects.get(id=scan_id)):
                    scan_operating_record = ScanOperatingRecord.objects.get(id_scan=Scan.objects.get(id=scan_id))
                    if scan_operating_record.liked == 1:
                        scan_operating_record.liked = 0;
                else:
                    scan_operating_record = ScanOperatingRecord.objects.create(id_scan=Scan.objects.get(id=scan_id))
                scan_operating_record.save()
        else:
            return HttpResponse('error')
    except Exception as e:
        logger.error(e)
        return HttpResponse('error')
    return HttpResponse('success')


# 获取点赞数api
def get_ar_like_api(request):
    try:
        bundle_id = request.GET.get('bundle_id')
        if bundle_id is not None and Bundle.objects.filter(id=bundle_id):
            bundle = Bundle.objects.get(id=bundle_id)
            likes = bundle.likes
        else:
            return HttpResponse('error')
    except Exception as e:
        logger.error(e)
        return HttpResponse('error')
    return HttpResponse(likes)


# 404
def page404(request):
    return render(request, '404.html')


@staff_member_required
def server(request):
    try:
        context = {
            'title': u'服务器监控',
        }
    except Exception as e:
        logger.error(e)
    return render_to_response('server.html', context, context_instance=RequestContext(request))


def server_info_api(request):
    try:
        server_info = get_server_info()
    except Exception as e:
        logger.error(e)
    return HttpResponse(json.dumps(server_info))


# test
def api_test(request):
    try:
        bundle_id = request.GET.get('bundle_id')
        ip = request.GET.get('ip')
        if ip is not None and bundle_id is not None and Bundle.objects.filter(id=bundle_id):
            url = 'http://ip.taobao.com/service/getIpInfo.php?ip=' + ip
            response = requests.get(url)
            data = location_handle(response.json())
            if not Locations.objects.filter(province=data['data']['region'], city=data['data']['city'],
                                            county=data['data']['county'], ):
                location = Locations.objects.create(province=data['data']['region'],
                                                    city=data['data']['city'],
                                                    county=data['data']['county'],
                                                    )
                location.save()
            else:
                location = Locations.objects.get(province=data['data']['region'],
                                                 city=data['data']['city'],
                                                 county=data['data']['county'],
                                                 )
            bundle = Bundle.objects.get(id=bundle_id)
            Scan.objects.create(id_bundle=bundle, id_location=location)
            config_info = bundle.config_info
            return HttpResponse(config_info)
    except Exception as e:
        logger.error(e)
    return HttpResponse('error')
