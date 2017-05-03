# -*- coding: utf-8 -*-
# @Time    : 2017/5/2 22:40
# @Author  : yj

from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment     #以Comment来生成表单
        fields = ('name','email','body')    #表明只有哪些字段显示在表单中