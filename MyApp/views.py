import logging
from django.shortcuts import render

logger = logging.getLogger('MyApp.views')

def index(request):
    return render(request,'index.html',locals())
