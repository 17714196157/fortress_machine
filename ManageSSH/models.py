from django.db import models

# Create your models here.

from django.contrib.auth.models import User


class Host(models.Model):
    hostname = models.CharField(max_length=64,verbose_name="主机名")
    ip = models.GenericIPAddressField(verbose_name="主机IP",unique=True)
    class Meta:
        verbose_name_plural="主机表"
    def __str__(self):
        return  self.hostname +":"+ self.ip


class HostGroup(models.Model):
    groupname = models.CharField(max_length=64,unique=True,verbose_name="主机组名")
    associated_host= models.ManyToManyField(Host,related_name="host_in_group")
    class Meta:
        verbose_name_plural="主机组表"
    def __str__(self):
        return  self.groupname

class LoginAccount(models.Model):
    choices =((0,"密码登陆方式"),(1,"密钥登陆方式"))
    mode = models.SmallIntegerField(choices=choices)
    accountname = models.CharField(max_length=64)
    passwd=models.CharField(max_length=64,blank=True,null=True)
    class Meta:
        verbose_name_plural="linux账号表"
        unique_together=(('mode','accountname'))
    def __str__(self):
        return  self.accountname   + str(self.mode)

class HostBindAccount(models.Model):
    host = models.ForeignKey(Host,related_name="host_of_bindhost",on_delete=models.CASCADE)
    account = models.ForeignKey(LoginAccount,related_name="account_of_bindhost",on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural="主机与账号绑定关系表"
        unique_together=(('host','account'))
    def __str__(self):
        return str(self.host) +":"+ str(self.account)

class  UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name="账号",on_delete=models.CASCADE)   #on_delete=models.CASCADE  级联删除表数据
    passwd = models.CharField(max_length=64, verbose_name="密码")
    tip = models.TextField(max_length=1024,blank=True, null=True, verbose_name="用户简介")
    hostlist = models.ManyToManyField(HostBindAccount,related_name="related_user",blank=True,null=True)

    class Meta:
        verbose_name_plural = "用户表"

    def __str__(self):
        return str(self.user)
