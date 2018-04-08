# encoding:utf-8
from __future__ import unicode_literals
from django import forms
from django.contrib.auth.models import User
#from helpers.director.model_func.dictfy import get_or_none
from django.contrib import auth 
from django.utils.translation import ugettext as _

class AuthForm(forms.ModelForm):
    pas2= forms.CharField(max_length=100,label=_('second password'))
    class Meta:
        model = User
        fields = ['username', 'password']
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        if not password:
            raise forms.ValidationError(_('need password'))
        return password
    
    def clean_pas2(self):
        password = self.data.get('password')
        pas2 = self.cleaned_data.get('pas2')
        if password != pas2:
            raise forms.ValidationError(_('two password should be same'))
        return pas2
        
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_('username has been exist'))
        return username
    
    def clean(self):
        if 'pas2' in self.cleaned_data:
            del self.cleaned_data['pas2']
        return self.cleaned_data


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
    
    def clean(self):
        username=self.cleaned_data.get('username')
        password=self.cleaned_data.get('password')
        user= auth.authenticate(username=username,password=password)
        if not username or not password:
            for k,v in self.errors.items():
                field = self.fields.get(k)
                if field.error_messages.has_key('required'):
                    self.errors[k]=['必须输入%s'%unicode(field.label),]
            return
        
        if user: 
            if user.is_active:
                return self.cleaned_data
                #auth.login(request, user)
            else:
                self.add_error('username',_('user has been disabled'))
        else:
            try:
                user=User.objects.get(username=username)
                self.add_error('username',_('user exist,but password not match'))
            except User.DoesNotExist:
                self.add_error('username',_('user not exist'))
        
    
    
    