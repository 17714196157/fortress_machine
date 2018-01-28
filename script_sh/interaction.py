from fortress_machine.settings import BASE_DIR
import sys,os
sys.path.append(BASE_DIR)

#脚本可以使用django的数据库以及其他模块 ，之前必须加上环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fortress_machine.settings")
import django
django.setup()

from django.contrib.auth import  authenticate
import subprocess
class Interface(object):
    def __init__(self):
        self.user = None
        self.dict_group_host = None

    def gethostgroup(self):
        '''
        计算当前登陆用户 有权限访问的主机 ，并安装主机组分类
        :return:
        '''
        self.dict_group_host = None
        hostaccountlist = self.user.userprofile.hostlist.all()
        len_hostaccountlist = len(hostaccountlist)
        dict_group_host={"NoGroup":[]}
        for hostaccount in  hostaccountlist:
            group_list = hostaccount.host.host_in_group.all()
            if len(group_list) == 0:
                dict_group_host["NoGroup"].append(hostaccount)
            for  group in  group_list:
                if group not in dict_group_host:
                    dict_group_host.update({group:[hostaccount]})
                else:
                    dict_group_host[group].append(hostaccount)
        self.dict_group_host =dict_group_host
        print("dict_group_host:",self.dict_group_host)
        pass

    def select_interactive(self,nodelist,tip="请选择需要XXXX的XX"):
        '''
        交互界面
        :param nodelist:
        :param tip:
        :return:
        '''
        len_nodelist = len(nodelist)
        list_node = []  #按顺序暂存序列里的元素
        for index , hostaccount in enumerate(nodelist):
            list_node.append(hostaccount)
        num = ""
        while num != "z":
            print(tip)
            len_nodelist = len(nodelist)
            for index , hostaccount in enumerate(list_node):
                print(index," ",hostaccount,type(hostaccount))

            num = input("#####################").strip()
            if num.isdigit()  and int(num) in range(len_nodelist):
                return list_node[int(num)]
            elif num == "z":
                return None
            else:
                print("输入超出范围 ，请重试")


    def Hostgroupmenu_interactive(self):
        groupnode_of_user =self.select_interactive(self.dict_group_host,"请选择需要登陆的主机组")
        if groupnode_of_user:
            print(groupnode_of_user)
            print("self.dict_group_host[groupnode_of_user]:",self.dict_group_host[groupnode_of_user])
            hostbindaccount_node = self.select_interactive(self.dict_group_host[groupnode_of_user],"请选择需要登陆的主机")
            if hostbindaccount_node :
                linux_username = hostbindaccount_node.account.accountname
                linux_passwd = hostbindaccount_node.account.passwd
                linux_ip = hostbindaccount_node.host.ip
                sshlogin_cmd = '''sshpass -p {linux_passwd} ssh {linux_username}@{linux_ip} -o "StrictHostKeyChecking no"  '''.format(
                        linux_ip=linux_ip,linux_passwd=linux_passwd,linux_username=linux_username)
                print("sshlogin_cmd:",sshlogin_cmd)
                #subprocess.run(sshlogin_cmd)
            else:
                self.Hostgroupmenu_interactive()
        else:
            self.interactive()

    def login_interactive(self):
        '''
        用户登陆认证交互界面
        :return:
        '''
        try_time = 0
        while try_time<3:
            try_time += 1
            username = input("请输入用户名").strip()
            passwd = input("请输入登陆密码").strip()

            username="qinyuchen"
            passwd="qq3@django"

            if username != "" and passwd !="":
                user = authenticate(username=username,password = passwd)
                print(user,type(user))
                if user:
                    print("登陆成功")
                    self.user = user
                    self.gethostgroup()
                    return True
                else:
                    print("登陆失败，请重试")
        else:
             print("登陆失败3次，自动退出")
             return  False

    def interactive(self):
        login_flag = self.login_interactive()
        if login_flag:
            self.Hostgroupmenu_interactive()


if __name__ == "__main__":
    lg =Interface()
    lg.interactive()