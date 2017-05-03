from django.shortcuts import render,get_object_or_404
from django.core.mail import send_mail
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Count
from django.views.generic import ListView
from .forms import EmailPostForm,CommentForm
from .models import Post,Comment
from taggit.models import Tag

# Create your views here.

# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'


def post_list(request,tag_slug=None): #列表
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list,3)    #每页显示3条
    page = request.GET.get('page')  #指明当前页数
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)    #如果页面不是一个整数交付第一页
    except EmptyPage:
        posts = paginator.page(paginator.num_pages) #如果页面范围交付最后一页的搜索结果
    return render(request,'blog/post/list.html',{'posts':posts,'page':page,'tag':tag})


def post_detail(request,year,month,day,post):   #详情
    post = get_object_or_404(Post,slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
    #此帖子的活动评论列表
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method =='POST':
        #发表了评论
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #创建评论对象，但不保存到数据库
            new_comment = comment_form.save(commit=False)
            #将当前帖子分配给评论
            new_comment.post = post
            #将评论保存到数据库
            new_comment.save()
    else:
        comment_form = CommentForm()

    post_tags_ids = post.tags.values_list('id',flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    return render(request,'blog/post/detail.html',{'post':post,
                                                   'comments':comments,
                                                   'new_comment':new_comment,
                                                   'comment_form':comment_form,
                                                   'similar_posts':similar_posts})


def post_share(request,post_id):
    post = get_object_or_404(Post,id=post_id,status = 'published')  #检索post的id
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{}({}) 建议你阅读 "{}"'.format(cd['name'],cd['email'],post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: "{}"'.format(post.title,post_url,cd['name'],cd['comments'])
            send_mail(subject, message, '809127232@qq.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post,'form':form,'sent':sent})

