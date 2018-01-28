from django.contrib import admin

# Register your models here.
from django.contrib import admin
from ManageSSH import models
admin.site.register(models.Host)
admin.site.register(models.UserProfile)
admin.site.register(models.HostBindAccount)
admin.site.register(models.HostGroup)
admin.site.register(models.LoginAccount)