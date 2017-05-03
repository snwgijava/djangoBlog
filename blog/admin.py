from django.contrib import admin
from .models import Post,Comment

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author','publish','status') #帖子列展示
    list_filter = ('status','created','publish','author')   #右侧边栏过滤
    search_fields = ('title','body')    #搜索框
    prepopulated_fields = {'slug':('title',)}      #通过标题填充slug字段
    raw_id_fields = ('author',) #作者字段展示为搜索
    date_hierarchy = 'publish'  #时间层快速导航
    ordering = ['status','publish'] #排序


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','post','created','active')
    list_filter = ('active','created','updated')
    search_fields = ('name','email','body')

admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
