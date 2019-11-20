from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import BookInfo
import pymysql
import time
from article_review_system.settings.dev import MYSQL_HOST,MYSQL_USERNAME,MYSQL_PASSWORD,DB_NAME,DB_PORT
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
    """修改功能"""
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

class DeleteData(View):
    """删除功能"""
    def get(self,request):
        """接收文章id，根据id删除对应的文章"""
        id = request.GET.get('id')
        BookInfo.objects.filter(id=id).delete()
        return redirect('/showdata/')


class PublishData(View):
    """发布功能"""
    def __init__(self):
        # 连接MySQL
        self.connect = pymysql.connect(host=MYSQL_HOST, port=DB_PORT, user=MYSQL_USERNAME, password=MYSQL_PASSWORD,
                                       db=DB_NAME)
        self.cursor = self.connect.cursor()
    def get(self,request):
        """接收前端发送的id,查询出id对应的content，然后写入到服务器中，根据文章id删除系统数据库文章"""
        id = request.GET.get('id')
        content = BookInfo.objects.get(id=id).content
        title=BookInfo.objects.get(id=id).title
        # 将item数据写入表www_kaifamei_com_ecms_news_check
        insert_sql_first = '''INSERT INTO www_kaifamei_com_ecms_news_check(classid,newspath,filename,title,titleurl,newstime) VALUES (4,"{}","100","{}","news/yxnews/{}/{}","{}")'''.format(
            time.strftime('%Y-%m-%d', time.localtime(time.time())), '(系统写入测试)'+title,
            time.strftime('%Y-%m-%d', time.localtime(time.time())), '2.html', int(time.time()))
        update_sql_first = '''UPDATE www_kaifamei_com_ecms_news_check SET filename=id'''
        # 将item数据写入表www_kaifamei_com_ecms_news_check_data
        insert_sql_second = '''INSERT INTO www_kaifamei_com_ecms_news_check_data(classid,dokey,newstext) VALUES (4,1,'{}')'''.format(
            content)
        # 将item数据写入表www_kaifamei_com_ecms_news_index
        insert_sql_third = '''INSERT INTO www_kaifamei_com_ecms_news_index(classid,lastdotime) VALUES (4,{})'''.format(
            int(time.time()))
        try:
            self.cursor.execute(insert_sql_first)
            self.cursor.execute(update_sql_first)
            self.cursor.execute(insert_sql_second)
            self.cursor.execute(insert_sql_third)
            self.connect.commit()
            BookInfo.objects.filter(id=id).delete()
            return redirect('/showdata/')
        except:
            pass