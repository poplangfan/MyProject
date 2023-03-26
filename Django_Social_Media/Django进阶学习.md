## Django进阶学习

基于`python3.8`和`Django4.1.3`的博客。   

### 学习新框架的一点小技巧

- 不要看太多教程，1~2个为佳，快速构建起来后，再适配、修改、拓展；

  > [Django 文档 | Django 文档 | Django (djangoproject.com)](https://docs.djangoproject.com/zh-hans/4.1/)
  >
  > [大江狗的博客 | 大江狗的技术及生活博客 (pythondjango.cn)](https://pythondjango.cn/)
  >
  > [liangliangyy/DjangoBlog: 🍺基于Django的博客系统 (github.com)](https://github.com/liangliangyy/DjangoBlog)




- 掌握框架的设计哲学和思想

    > The web framework for perfectionists with deadlines.
    >
    > Django 是一个高级 Python Web 框架，它鼓励快速开发和干净、务实的设计。 由经验丰富的开发人员构建，它解决了Web开发的大部分麻烦，因此您可以集中精力 编写应用程序时无需重新发明轮子。它是免费和开源的。
    >
    >



### 三步走策略

#### step1

了解当前参考的项目，能正常运行

#### step2

改造成我们需要的样子

#### step3

熟练掌握、拓展全新的功能



###  学习内容

####  day 0 2023/03/12  内容介绍

- [x] 本次内容介绍，项目启动：`python .\manage.py runserver`


####  day 1 2023/03/20  数据库变更为PostgreSQL

- [x] 数据库变更为PostgreSQL， 本次操作以windows为例，linux大部分一致，小部分差异自行查阅资料解决。后续开发差不多也会切换到linux上去

##### 下载与安装

[下载地址](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)

我下载的版本是：`postgresql-14.7-1-windows-x64.exe`

tips：下载完成后，执行exe安装包安装，过程中会让你设置管理员密码`123456`，和给一个默认的端口号`5432`，并且可以选择一些安装包，我选择了pgAdmin数据库管理工具，这样就可以直接管理数据库了。

##### 创建数据库与启动

###### 创建数据库

1、通过pgAdmin创建

2、通过命令行创建，本人采用此种方式，软件安装完成后，会有SQL Shell直接打开即可

![1679319229074](C:\Users\11577\AppData\Roaming\Typora\typora-user-images\1679319229074.png)



```sql
# 创建名为socialbook的数据库
CREATE DATABASE socialbook; 
# 创建用户名和密码
CREATE USER myuser WITH ENCRYPTED PASSWORD '123456'; 
# 给创建的用户授权
GRANT ALL PRIVILEGES ON DATABASE socialbook TO myuser;

# 以下设置可手动进行设置，也可以在postgresql.conf中进行配置
# 设置客户端字符为utf-8，防止乱码
ALTER ROLE myuser SET client_encoding TO 'utf8';
# 事务相关设置 - 推荐
ALTER ROLE myuser SET default_transaction_isolation TO 'read committed';
# 设置数据库时区为UTC - 推荐
ALTER ROLE myuser SET timezone TO 'UTC';
```



然后就是登陆过程了，首先是 `Server`，也就是说数据库 url，默认是在本地（所以是 `localhost`），没有该动的就直接回车下一步好了。

接着是 `Database`，也即我们数据库，这里默认是使用 `postgres`，因为我们是第一次登陆，所以这里也就直接回车下一步就好了。

再接着是 `Port`，也就是端口号，默认是 5432，如果你安装的时候改动了，那么此时你最好也改成你当时改的端口，否则可能导致连接失败。

然后是 `Username`，也就是 PostgreSQL 的用户，这里一般默认是超级用户（`postgres`，这里不同于 MySQL 的 `root`，要注意），而我们也是第一次登陆，没有建立新账户，直接默认回车下一步即可。

最后要输入的则是口令，也就是登陆数据库的密码，这里我们已经在上边设置过了，直接输入后回车即可。

如果我们登陆成功，那么就会出现下面图中的提示了。

![1679319516608](C:\Users\11577\AppData\Roaming\Typora\typora-user-images\1679319516608.png)

###### 启动服务

进入bin所在目录，执行：`pg_ctl start -w -D  "D:\devsoft\postgresql\data"`

##### 设置与调试

要让Python与Postgres一起工作，你需要安装“psycopg2”模块

`pip install psycopg2`

修改项目文件夹里的`settings.py`的文件，添加创建的数据库和用户信息。

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',   # 数据库引擎
        'NAME': 'mydb',         # 数据库名，Django不会帮你创建，需要自己进入数据库创建。
        'USER': 'myuser',     # 设置的数据库用户名
        'PASSWORD': 'mypass',     # 设置的密码
        'HOST': 'localhost',    # 本地主机或数据库服务器的ip
        'PORT': '',         # 数据库使用的端口
    }
}
```

设置好后，连续使用如下命令如果没有出现错误，就可以在Django项目中使用PostgreSQL数据库。得益于优秀的ORM设计，更换数据库不需要动任何代码。

```python
python manage.py makemigrations                                                              
python manage.py migrate
```

#### day 2 2023/03/26  支持Redis缓存

- [ ] 支持`Redis`缓存，支持缓存自动刷新。

Django缓存设置分为很多种，我们以Redis为例，其它请查看：[Django多种缓存配置方式 | 大江狗的博客 (pythondjango.cn)](https://pythondjango.cn/django/advanced/7-cache/#redis%E7%BC%93%E5%AD%98)

- Memcached缓存
- Redis缓存
- 数据库缓存
- 文件系统缓存
- 本地内存缓存
- Dummy缓存

##### 下载与安装

[Redis 官网](https://redis.io/)

[Releases · tporadowski/redis (github.com) 下载地址](https://github.com/tporadowski/redis/releases)

##### 启动服务
打开一个 cmd 窗口 使用 cd 命令切换redis目录运行：
`redis-server.exe redis.windows.conf`

##### 配置与调试
Redis安装好并且启动后，你还需要通过pip安装django-redis才能在Django中操作redis数据库。
`pip install django-redis`



setting.py设置

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
            # "PASSWORD": "密码",
            "DECODE_RESPONSES": True
        }
    },
}
```

##### 多种缓存方式尝试

###### 全站缓存
全站缓存(per-site)是依赖中间件实现的，也是Django项目中使用缓存最简单的方式。这种缓存方式仅适用于静态网站或动态内容很少的网站。
```python
# 缓存中间件，添加顺序很重要
MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',     # 新增
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',  # 新增
]
```



###### 在视图View中使用

此种缓存方式依赖@cache_page这个装饰器，仅适合内容不怎么变化的单个视图页面。
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)
def my_view(request):
```



######  路由URLConf中使用

同样@cache_page这个装饰器，只不过在urls.py中使用。
```python
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('articles/<int:id>/', cache_page(60 * 15)(my_view)),
]
```




#### day 3

- [ ] 支持Oauth登陆，现已有Google,GitHub,facebook,微博,QQ登录。

...

#### day 20
- [ ] 
```

```