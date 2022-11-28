from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages


# 登录
def signin(request):
    # 如果是post请求
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        # 校验
        user = auth.authenticate(username=username, password=password)
        # 如果用户存在
        if user is not None:
            messages.info(request, '登录成功')
            return redirect('signin')
        # 如果用户不存在
        else:
            messages.info(request, '登录失败')
            return redirect('signin')
    # 如果不是post请求
    else:
        return render(request, 'signin.html')


# 注册
def signup(request):
    # 如果是post请求
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # 如果密码相等
        if password == password2:
            # 如果邮箱已存在
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Taken")
                return redirect('signup')
            # 如果用户名已经存在
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Taken")
                return redirect('signup')
            # 如果都不存在
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                messages.info(request, '注册成功')
                return redirect('signup')
        # 如果密码不等，提示
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
    # 如果请求不是post，保持在注册界面
    else:
        return render(request, 'signup.html')
