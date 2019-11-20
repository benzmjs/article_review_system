from django.db import models


class BookInfo(models.Model):
    """定义文章信息模型类"""
    title=models.CharField(max_length=50)
    content=models.TextField()

    class Meta:
        db_table = 'article_data'  # 指明数据库表名

