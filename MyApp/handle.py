# -*- coding: utf-8 -*-
from django.conf import settings
import json


def api_url_maker(bundle_id):
    url = settings.SITE_URL + '/arConfigInfo-api?bundle_id=' + bundle_id
    return url


def target_image_url_maker(target_image):
    url = settings.SITE_URL + target_image.url
    return url


def prefab_url_maker(prefab):
    url = settings.SITE_URL + prefab.url
    return url


def ar_config_info_handle(target_image, prefab):
    target_image_url = target_image_url_maker(target_image)
    prefab_url = prefab_url_maker(prefab)

    data = {
        'targetImageUrl': target_image_url,
        'prefabUrl': prefab_url,
    }

    jsonData = json.dumps(data)

    return jsonData


def location_handle(data):
    data['data']['region'] = data['data']['region'].replace(u'省', '')
    data['data']['region'] = data['data']['region'].replace(u'市', '')
    data['data']['region'] = data['data']['region'].replace(u'特别行政区', '')
    data['data']['city'] = data['data']['city'].replace(u'北京市', '')
    data['data']['city'] = data['data']['city'].replace(u'天津市', '')
    data['data']['city'] = data['data']['city'].replace(u'重庆市', '')
    data['data']['city'] = data['data']['city'].replace(u'上海市', '')
    return data
