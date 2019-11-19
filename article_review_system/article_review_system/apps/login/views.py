from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View


class Login(View):
    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
        # 接受参数
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        # 认证登录用户
        user = authenticate(username=username, password=password)
        if user is  None:
            content={"message":"账户或密码错误"}
            return render(request, 'login.html',content)
        # 实现状态保持
        login(request, user)
        # 设置状态保持的周期
        request.session.set_expiry(None)
        # 响应登录结果
        return redirect('/showdata/')