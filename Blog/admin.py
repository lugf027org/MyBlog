from django.contrib import admin
from . import models


class TagInline(admin.TabularInline):
    model = models.Tag


class ArticleAdmin(admin.ModelAdmin):
    inlines = [TagInline]  # Inline
    list_display = ('文章标题', '文章摘要', '发布时间', )  # list
    search_fields = ('文章标题',)
    fieldsets = (
        ['Main', {
            'fields': ('文章标题', '正文内容'),
        }],
        ['Advance', {
            'classes': ('collapse',),
            'fields': ('文章摘要',),
        }]
    )


admin.site.register(models.Articles, ArticleAdmin)

