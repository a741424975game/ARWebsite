# -*- coding: utf-8 -*-
from MyApp.models import *
from calendar import monthrange
import datetime
import json


# 单个模型最近访问和评论数量
class DailyVC:
    recently_days = []

    recently_visits_amount = []

    recently_comments_amount = []

    def __init__(self, id_bundle):
        self.recently_days = []
        self.recently_visits_amount = []
        self.recently_comments_amount = []
        today = datetime.date.today()
        i = 5
        while i >= 0:
            day_delta = datetime.timedelta(days=i)
            self.recently_days.append(today - day_delta)
            i -= 1
        for eachDay in self.recently_days:
            if ScanStatistics.objects.filter(id_bundle=id_bundle, datetime=eachDay):
                scan_statistics = ScanStatistics.objects.get(id_bundle=id_bundle, datetime=eachDay)
                self.recently_visits_amount.append(scan_statistics.amount)
            else:
                self.recently_visits_amount.append(0)

            if CommentStatistics.objects.filter(id_bundle=id_bundle, datetime=eachDay):
                comment_statistics = CommentStatistics.objects.get(id_bundle=id_bundle, datetime=eachDay)
                self.recently_comments_amount.append(comment_statistics.amount)
            else:
                self.recently_comments_amount.append(0)
        temp = []
        for eachDay in self.recently_days:
            temp.append(str(eachDay))
        self.recently_days = json.dumps(temp)
        self.recently_visits_amount = json.dumps(self.recently_visits_amount)
        self.recently_comments_amount = json.dumps(self.recently_comments_amount)


# 单个模型区域访问量
class AreaVisits:
    area_visits = {}

    max = 0

    area_visits_ranking = []

    area_visits_ranking_data = []

    def __init__(self, id_bundle):
        self.area_visits = {}
        self.area_visits_ranking = []
        self.area_visits_ranking_data = []
        if ScanLocation.objects.filter(id_bundle=id_bundle):
            province_visits_amount = {}
            for eachScanLocation in ScanLocation.objects.filter(id_bundle=id_bundle):
                province = eachScanLocation.id_location.province
                city = eachScanLocation.id_location.city
                county = eachScanLocation.id_location.county
                amount = eachScanLocation.amount
                if province != '':
                    if self.area_visits.has_key(province):
                        self.area_visits[province] += amount
                        province_visits_amount[province] += amount
                    else:
                        self.area_visits[province] = amount
                        province_visits_amount[province] = amount
                    if city != '':
                        if self.area_visits.has_key(city):
                            self.area_visits[city] += amount
                        else:
                            self.area_visits[city] = amount
                    elif county != '':
                        if self.area_visits.has_key(county):
                            self.area_visits[county] += amount
                        else:
                            self.area_visits[county] = amount
            if len(province_visits_amount) < 5:
                temp = sorted(province_visits_amount.items(), key=lambda d: d[1], reverse=True)[
                       0: len(province_visits_amount)]
            else:
                temp = sorted(province_visits_amount.items(), key=lambda d: d[1], reverse=True)[0:5]
            self.max = temp[0][1]
            for each_tuple in temp:
                self.area_visits_ranking.append(each_tuple[0])
                self.area_visits_ranking_data.append(each_tuple[1])
            temp = []
            for key, value in self.area_visits.items():
                tempDic = {'name': key, 'value': value}
                temp.append(tempDic)
            self.area_visits = json.dumps(temp)
            self.area_visits_ranking = json.dumps(self.area_visits_ranking)
            self.area_visits_ranking_data = json.dumps(self.area_visits_ranking_data)
        else:
            self.area_visits = []


# 单个模型最近月访问和评论数量
class MonthlyVC:
    recently_months = []

    recently_months_visits_amount = [0, 0, 0, 0, 0, 0]

    recently_months_comments_amount = [0, 0, 0, 0, 0, 0]

    def __init__(self, id_bundle):
        self.recently_months = []
        self.recently_months_visits_amount = [0, 0, 0, 0, 0, 0]
        self.recently_months_comments_amount = [0, 0, 0, 0, 0, 0]
        date = datetime.datetime.today()
        self.recently_months.append(date)
        for i in range(0, 5):
            date = date - datetime.timedelta(days=monthrange(date.year, date.month)[1])
            self.recently_months.append(date)
        self.recently_months.reverse()
        if ScanStatistics.objects.filter(id_bundle=id_bundle):
            for each_scan in ScanStatistics.objects.filter(id_bundle=id_bundle):
                for i in range(0, 6):
                    if each_scan.datetime.year == self.recently_months[i].year and each_scan.datetime.month == \
                            self.recently_months[i].month:
                        self.recently_months_visits_amount[i] += each_scan.amount
        if CommentStatistics.objects.filter(id_bundle=id_bundle):
            for each_comment in CommentStatistics.objects.filter(id_bundle=id_bundle):
                for i in range(0, 6):
                    if each_comment.datetime.year == self.recently_months[i].year and each_comment.datetime.month == \
                            self.recently_months[i].month:
                        self.recently_months_comments_amount[i] += each_comment.amount
        temp = []
        for each_date in self.recently_months:
            temp.append(str(each_date.year) + '-' + str(each_date.month))
        self.recently_months = json.dumps(temp)
        self.recently_months_visits_amount = json.dumps(self.recently_months_visits_amount)
        self.recently_months_comments_amount = json.dumps(self.recently_months_comments_amount)


# 所有模型最近月访问量
class MonthlyVisits:
    recently_months = []

    recently_months_visits_amount = [0, 0, 0, 0, 0, 0]

    def __init__(self, username):
        self.recently_months = []
        self.recently_months_visits_amount = [0, 0, 0, 0, 0, 0]
        date = datetime.datetime.today()
        self.recently_months.append(date)
        for i in range(0, 5):
            date = date - datetime.timedelta(days=monthrange(date.year, date.month)[1])
            self.recently_months.append(date)
        self.recently_months.reverse()
        for bundle in User.objects.get(username=username).bundle_set.all():
            scan_statistics = bundle.scanstatistics_set.all()
            for each_scan in scan_statistics:
                for i in range(0, 6):
                    if each_scan.datetime.year == self.recently_months[i].year and each_scan.datetime.month == \
                            self.recently_months[i].month:
                        self.recently_months_visits_amount[i] += each_scan.amount
        temp = []
        for each_date in self.recently_months:
            temp.append(str(each_date.year) + '-' + str(each_date.month))
        self.recently_months = json.dumps(temp)
        self.recently_months_visits_amount = json.dumps(self.recently_months_visits_amount)


# 所有模型的区域访问量排行:
class RegionRank:
    area_visits_ranking = []

    area_visits_ranking_data = []

    def __init__(self, username):
        self.area_visits_ranking = []
        self.area_visits_ranking_data = []
        province_visits_amount = {}
        for bundle in User.objects.get(username=username).bundle_set.all():
            scan_locations = bundle.scanlocation_set.all()
            for each_location in scan_locations:
                province = each_location.id_location.province
                amount = each_location.amount
                if province != '':
                    if province_visits_amount.has_key(province):
                        province_visits_amount[province] += amount
                    else:
                        province_visits_amount[province] = amount
        if len(province_visits_amount) < 5:
            temp = sorted(province_visits_amount.items(), key=lambda d: d[1], reverse=True)[
                   0: len(province_visits_amount)]
        else:
            temp = sorted(province_visits_amount.items(), key=lambda d: d[1], reverse=True)[0:5]
        for each_tuple in temp:
            self.area_visits_ranking.append(each_tuple[0])
            self.area_visits_ranking_data.append(each_tuple[1])
        self.area_visits_ranking = json.dumps(self.area_visits_ranking)
        self.area_visits_ranking_data = json.dumps(self.area_visits_ranking_data)


