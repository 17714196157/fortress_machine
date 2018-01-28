# Generated by Django 2.0 on 2018-01-28 05:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=64, verbose_name='主机名')),
                ('ip', models.GenericIPAddressField(unique=True, verbose_name='主机IP')),
            ],
            options={
                'verbose_name_plural': '主机表',
            },
        ),
        migrations.CreateModel(
            name='HostBindAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': '主机与账号绑定关系表',
            },
        ),
        migrations.CreateModel(
            name='HostGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupname', models.CharField(max_length=64, unique=True, verbose_name='主机组名')),
                ('associated_host', models.ManyToManyField(related_name='host_in_group', to='ManageSSH.Host')),
            ],
            options={
                'verbose_name_plural': '主机组表',
            },
        ),
        migrations.CreateModel(
            name='LoginAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode', models.SmallIntegerField(choices=[(0, '密码登陆方式'), (1, '密钥登陆方式')])),
                ('accountname', models.CharField(max_length=64)),
                ('passwd', models.CharField(blank=True, max_length=64, null=True)),
            ],
            options={
                'verbose_name_plural': 'linux账号表',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passwd', models.CharField(max_length=64, verbose_name='密码')),
                ('tip', models.TextField(blank=True, max_length=1024, null=True, verbose_name='用户简介')),
                ('hostlist', models.ManyToManyField(blank=True, null=True, related_name='related_user', to='ManageSSH.HostBindAccount')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='账号')),
            ],
            options={
                'verbose_name_plural': '用户表',
            },
        ),
        migrations.AlterUniqueTogether(
            name='loginaccount',
            unique_together={('mode', 'accountname')},
        ),
        migrations.AddField(
            model_name='hostbindaccount',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_of_bindhost', to='ManageSSH.LoginAccount'),
        ),
        migrations.AddField(
            model_name='hostbindaccount',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='host_of_bindhost', to='ManageSSH.Host'),
        ),
        migrations.AlterUniqueTogether(
            name='hostbindaccount',
            unique_together={('host', 'account')},
        ),
    ]