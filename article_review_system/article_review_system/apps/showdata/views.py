from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


class Showdata(View):

    def get(self,request):
        if request.user.is_authenticated():
            return HttpResponse("成功登陆显示数据")
        else:
            return  HttpResponse("请登录")