from django.db import models
from mdeditor.fields import MDTextField
import django.utils.timezone as timezone


class Articles(models.Model):
    文章标题 = models.CharField(max_length=32)
    文章摘要 = models.TextField(default='无摘要')
    发布时间 = models.DateTimeField(default=timezone.now)
    正文内容 = MDTextField()


class Tag(models.Model):
    contact = models.ForeignKey(Articles, on_delete=models.CASCADE)
    标签 = models.CharField(max_length=50)

    def __unicode__(self):
        return self.标签
