# -*- coding: utf-8 -*-
from django import forms
from MyApp.models import *

# register form 注册表单
class RegisterForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","id":"userName","type":"text","placeholder": "User Name", "required": "required",}),
                                min_length=3,max_length=30, error_messages={"required": "username 不能为空",})

    email = forms.EmailField(widget=forms.TextInput(attrs={"class":"form-control","id":"email","placeholder": "Email", "type":"email","required": "required",}),
                                max_length=50, error_messages={"required": "email 不能为空",})

    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","id":"Password1","placeholder": "Password", "type":"password","required": "required",}),
                                min_length=8,max_length=30, error_messages={"required": "password 不能为空",})


    rePassword = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","id":"Password2","placeholder": "Password", "type":"password","required": "required",}),
                                min_length=8,max_length=30, error_messages={"required": "password 不能为空",})

    def clean_rePassword(self):
        password = self.cleaned_data.get('password')
        rePassword = self.cleaned_data.get('rePassword')
        if rePassword != password:
            raise forms.ValidationError("两次输入的密码不一致")
        return rePassword

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username):
            raise forms.ValidationError("用户名已存在")
        return username

# login form 登录表单
class LoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "id": "userName", "type": "text", "placeholder": "User Name","required": "required",}),
                            min_length=3, max_length=30, error_messages={"required": "username 不能为空",})

    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "id": "Password1", "placeholder": "Password", "type": "password","required": "required",}),
                            min_length=8, max_length=30, error_messages={"required": "password 不能为空",})

# upload form 上传表单
class UploadForm(forms.Form):

    modelName = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "id": "modelName", "type": "text", "placeholder": "Model Name","required": "required",}),
                            max_length=30, error_messages={"required": "modelName 不能为空",})

    note = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "id": "modelName", "type": "text", "placeholder": "Model Name",}))

    model = forms.FileField()

    imageTarget = forms.ImageField()