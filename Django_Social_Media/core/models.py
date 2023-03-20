from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()


class Profile(models.Model):
    # 当前操作的用户
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    # 个人介绍
    bio = models.TextField(blank=True)
    # 头像
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    # 地域
    location = models.CharField(max_length=100, blank=True)


# 博文，帖子
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    # 用户名
    user = models.CharField(max_length=100)
    # 发的帖子图片
    image = models.ImageField(upload_to='post_images')
    # 标题
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    # 点赞数
    no_of_likes = models.IntegerField(default=0)


class LikePost(models.Model):
    # 文章id
    post_id = models.CharField(max_length=500)
    # 用户名
    username = models.CharField(max_length=100)


class FollowersCount(models.Model):
    # 跟随者
    follower = models.CharField(max_length=100)
    # 用户
    user = models.CharField(max_length=100)
