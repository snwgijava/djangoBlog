from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager     #第三方标签库

# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft','草稿'),
        ('published','发布'),
    )
    title = models.CharField(max_length=200)    #标题
    slug = models.SlugField(max_length=250,unique_for_date='publish')   #在URLS中使用，一个短标签
    author = models.ForeignKey(User,related_name='blog_posts')  #作者
    body = models.TextField()   #文章
    publish = models.DateTimeField(default=timezone.now)    #发布时间
    created = models.DateTimeField(auto_now_add=True)   #创建时间
    updated = models.DateTimeField(auto_now=True)   #更新时间
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft') #展示状态
    tags = TaggableManager()    #第三方标签库

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):     #使用名字和可选参数构建URLs
        return reverse('blog:post_dateil',args=[self.publish.year,
                                                self.publish.strftime('%m'),
                                                self.publish.strftime('%d'),
                                                self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)  #评论是否显示

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} to on {}'.format(self.name,self.post)



