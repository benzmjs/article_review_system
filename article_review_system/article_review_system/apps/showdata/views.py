from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import BookInfo


class Showdata(View):

    def get(self, request):
        if request.user.is_authenticated():
            article_QuerySet = BookInfo.objects.all()
            data_dict = {str(every_article.id): every_article.title for every_article in article_QuerySet}
            context = {
                'all_article_info': data_dict
            }
            return render(request, 'showdata.html', context=context)
        else:
            return render(request, 'login.html')


class UpdateData(View):
    def get(self, request):
        "接收id，返回文章内容数据"
        id = request.GET.get('id')
        content = BookInfo.objects.get(id=id).content
        data={
            "id":id,
            "info":content
        }
        return render(request, 'shadiao.html',data)

    def post(self, request):
        """接收文章id和文章内容，根据id修改数据库中的content，修改完成后重定向到首页也就是showdata页面"""
        id = request.GET.get('id')
        content=request.POST.get('textarea')
        BookInfo.objects.filter(id=id).update(content=content)
        return redirect('/showdata/')