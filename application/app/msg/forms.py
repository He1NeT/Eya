#!/usr/bin/env python
#coding:utf-8

from django import forms
from captcha.fields import CaptchaField
from app.msg.models import Message
from app.tao.models import Images

class MessageForm(forms.ModelForm):
    message = forms.CharField(required=True)
    face = forms.CharField(required=True)
    content = forms.CharField(required=True)
    
    def clean_message(self):
        p = self.cleaned_data.get('message', None)
        if p is not None:
            return Images.objects.get(pk=p)
                    
    class Meta:
        model = Message
        fields = ['message','face', 'content']
