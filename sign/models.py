from django.db import models
from django.contrib.auth.models import User,AbstractUser,Group


class Userprofile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField('姓名',max_length=32,blank=True,null=False)
    groups = models.ManyToManyField("UserGroup")


    class Meta:
        verbose_name = '用户详情'
        verbose_name_plural = '用户详情'

    def __str__(self):
        return self.name

class UserGroup(models.Model):
    '''用户组表'''
    name = models.CharField(max_length=64, unique=True)
    def __unicode__(self):
        return self.name

class User_ex(models.Model):
    pass
# class MyUser(AbstractUser): # 继承AbstractUser类，实际上django的User也是继承他，我们要做的就是用自己的类代替django自己的User
#     name = models.CharField(u'中文名', max_length=32, blank=False, null=False)
#
#     class Meta:
#         verbose_name = u'用户详情'
#         verbose_name_plural = u"用户详情"

# class User_ex(AbstractUser):
#     name =



# Create your models here.
# 发布会
class Event(models.Model):
    name = models.CharField('发布会名称',max_length=100)            # 发布会标题
    limit = models.IntegerField('容纳用户数')                      # 限制人数
    status = models.BooleanField('状态')                     # 状态
    address = models.CharField('地址',max_length=200)         # 地址
    start_time = models.DateTimeField('发布会时间')   # 发布会时间events time
    create_time = models.DateTimeField(auto_now=True)  # 创建时间（自动获取当前时间）

    def __str__(self):
        return self.name


# 嘉宾
class Guest(models.Model):
    event = models.ForeignKey(Event)            # 关联发布会id
    realname = models.CharField('姓名',max_length=64)  # 姓名
    phone = models.CharField('手机号',max_length=16)     # 手机号
    email = models.EmailField('邮箱')                 # 邮箱
    sign = models.BooleanField('签到状态')                # 签到状态
    create_time = models.DateTimeField('创建时间',auto_now=True)  # 创建时间（自动获取当前时间）

    class Meta:
        unique_together = ('phone', 'event')

    def __str__(self):
        return self.realname


# 修改创建时间类型
# ALTER TABLE  `sign_event` CHANGE  `create_time`  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
# ALTER TABLE  `sign_guest` CHANGE  `create_time`  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

#用户管理
