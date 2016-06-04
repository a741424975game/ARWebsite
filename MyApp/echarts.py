from MyApp.models import *
import datetime
import json


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


class AreaVisits:
    area_visits = {}

    max = 0

    def __init__(self, id_bundle):
        self.area_visits = {}
        if ScanLocation.objects.filter(id_bundle=id_bundle):
            for eachScanLocation in ScanLocation.objects.filter(id_bundle=id_bundle):
                province = eachScanLocation.id_location.province
                city = eachScanLocation.id_location.city
                county = eachScanLocation.id_location.county
                amount = eachScanLocation.amount
                if province != '':
                    if self.area_visits.has_key(province):
                        self.area_visits[province] += amount
                    else:
                        self.area_visits[province] = amount
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
            temp = []
            for key, value in self.area_visits.items():
                if value > self.max:
                    self.max = value
                tempDic = {'name': key, 'value': value}
                temp.append(tempDic)
            self.area_visits = json.dumps(temp)


