from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from itertools import chain
import random

from .models import Profile, Post, LikePost, FollowersCount


@login_required(login_url='signin')
def index(request):
    # 获取当前活跃用户的基本信息
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []
    # 筛选出该用户的正在关注的人
    user_following = FollowersCount.objects.filter(follower=request.user.username)
    for users in user_following:
        user_following_list.append(users.user)
    # 筛选出所有正在关注的人的所有帖子
    post = []
    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        post.append(feed_lists)

    post_list = list(chain(*post))

    # 筛选出所有的可以关注的人
    # #筛选出所有人
    all_users = User.objects.all()

    # #筛选出所有正在关注的人
    user_following_all = []
    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    # #除掉已经关注的人
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    # #除掉自己
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]

    # 打乱顺序
    random.shuffle(final_suggestions_list)

    # 获取最终列表用户的个人信息
    # #获取id
    username_profile = []
    username_profile_list = []
    for users in final_suggestions_list:
        username_profile.append(users.id)
    # #获取信息
    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))
    return render(request, 'index.html', {'user_profile': user_profile, 'posts': post_list,
                                          'suggestions_username_profile_list': suggestions_username_profile_list[:4]})


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
            # messages.info(request, '登录成功')
            # return redirect('signin')
            auth.login(request, user)
            return redirect('/')
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

                # 登录
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                # 设置默认的个人信息
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                # 跳转到设置个人信息界面
                return redirect('settings')
        # 如果密码不等，提示
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
    # 如果请求不是post，保持在注册界面
    else:
        return render(request, 'signup.html')


@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        if not request.FILES.get('image'):
            user_profile.bio = request.POST['bio']
            user_profile.location = request.POST['location']
            user_profile.save()

        if request.FILES.get('image'):
            user_profile.profileimg = request.FILES.get('image')
            user_profile.bio = request.POST['bio']
            user_profile.location = request.POST['location']
            user_profile.save()
        return redirect('settings')
    return render(request, 'setting.html', {'user_profile': user_profile})


@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        # 模糊查询 忽略大小写 icontains
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        # 搜索到的人的基本信息列表
        username_profile_list = []
        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html',
                  {'user_profile': user_profile, 'username_profile_list': username_profile_list})


@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def profile(request, pk):
    # 用户对象
    user_object = User.objects.get(username=pk)
    # 用户基本信息
    user_profile = Profile.objects.get(user=user_object)
    # 用户帖子
    user_posts = Post.objects.filter(user=pk)
    # 用户帖子数
    user_post_length = len(user_posts)

    # 当前用户
    follower = request.user.username
    # 查询的用户
    user = pk
    # 如果有查到的，说明已经关注过，只能进行取消关注操作
    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    # 反之同理
    else:
        button_text = 'Follow'

    # 查询查询的用户的关注者，跟随者
    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'profile.html', context)


@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        # 操作者，当前用户
        follower = request.POST['follower']
        # 查看的人
        user = request.POST['user']

        # 删除一条数据
        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/' + user)
        # 新增一条数据
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/' + user)
    else:
        return redirect('/')


@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    # 被这个用户喜欢 +1
    if not like_filter:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        return redirect('/')
    # 没有被这个用户喜欢 -1
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        return redirect('/')
