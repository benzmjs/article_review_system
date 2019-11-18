from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


class Login(View):
    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
        # 接受参数
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        print(username)
        print(password)
        return HttpResponse("卧槽无情")
