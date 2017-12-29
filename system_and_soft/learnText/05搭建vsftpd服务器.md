centos7
1、关闭firewall：

systemctl stop firewalld.service #停止firewall

systemctl disable firewalld.service #禁止firewall开机启动

2、安装iptables防火墙

yum install iptables-services #安装

vi /etc/sysconfig/iptables #编辑防火墙配置文件

# Firewall configuration written by system-config-firewall

# Manual customization of this file is not recommended.

*filter

:INPUT ACCEPT [0:0]

:FORWARD ACCEPT [0:0]

:OUTPUT ACCEPT [0:0]

-A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

-A INPUT -p icmp -j ACCEPT

-A INPUT -i lo -j ACCEPT

-A INPUT -m state --state NEW -m tcp -p tcp --dport 22 -j ACCEPT

-A INPUT -m state --state NEW -m tcp -p tcp --dport 21 -j ACCEPT

-A INPUT -m state --state NEW -m tcp -p tcp --dport 10060:10090 -j ACCEPT

-A INPUT -j REJECT --reject-with icmp-host-prohibited

-A FORWARD -j REJECT --reject-with icmp-host-prohibited

COMMIT

:wq! #保存退出

systemctl restart iptables.service #最后重启防火墙使配置生效

systemctl enable iptables.service #设置防火墙开机启动

说明：21端口是ftp服务端口；10060到10090是Vsftpd被动模式需要的端口，可自定义一段大于1024的tcp端口。

系统运维  www.osyunwei.com  温馨提醒：qihang01原创内容?版权所有,转载请注明出处及原文链接

二、关闭SELINUX

vi /etc/selinux/config

#SELINUX=enforcing #注释掉

#SELINUXTYPE=targeted #注释掉

SELINUX=disabled #增加

:wq! #保存退出

setenforce 0 #使配置立即生效

三、安装vsftpd

yum install -y vsftpd #安装vsftpd

yum install -y psmisc net-tools systemd-devel libdb-devel perl-DBI  #安装vsftpd虚拟用户配置依赖包

systemctl start vsftpd.service #启动

systemctl enable vsftpd.service #设置vsftpd开机启动

四、配置vsftp服务器

cp /etc/vsftpd/vsftpd.conf /etc/vsftpd/vsftpd.conf-bak #备份默认配置文件

执行以下命令进行设置

sed -i "s/anonymous_enable=YES/anonymous_enable=NO/g" '/etc/vsftpd/vsftpd.conf'

sed -i "s/#anon_upload_enable=YES/anon_upload_enable=NO/g" '/etc/vsftpd/vsftpd.conf'

sed -i "s/#anon_mkdir_write_enable=YES/anon_mkdir_write_enable=YES/g" '/etc/vsftpd/vsftpd.conf'

sed -i "s/#chown_uploads=YES/chown_uploads=NO/g" '/etc/vsftpd/vsftpd.conf'

sed -i "s/#async_abor_enable=YES/async_abor_enable=YES/g" '/etc/vsftpd/vsftpd.conf'

sed -i "s/#ascii_upload_enable=YES/ascii_upload_enable=YES/g" '/etc/vsftpd/vsftpd.conf'

sed -i "s/#ascii_download_enable=YES/ascii_download_enable=YES/g" '/etc/vsftpd/vsftpd.conf'

sed -i "s/#ftpd_banner=Welcome to blah FTP service./ftpd_banner=Welcome to FTP service./g" '/etc/vsftpd/vsftpd.conf'

echo -e "use_localtime=YES\nlisten_port=21\nchroot_local_user=YES\nidle_session_timeout=300
\ndata_connection_timeout=1\nguest_enable=YES\nguest_username=vsftpd
\nuser_config_dir=/etc/vsftpd/vconf\nvirtual_use_local_privs=YES
\npasv_min_port=10060\npasv_max_port=10090
\naccept_timeout=5\nconnect_timeout=1" >> /etc/vsftpd/vsftpd.conf

五、建立虚拟用户名单文件

touch /etc/vsftpd/virtusers

编辑虚拟用户名单文件：（第一行账号，第二行密码，注意：不能使用root做用户名，系统保留）

vi /etc/vsftpd/virtusers
----------------
web1
123456
web2
123456
web3
123456
-----------------
:wq! #保存退出

六、生成虚拟用户数据文件

db_load -T -t hash -f /etc/vsftpd/virtusers /etc/vsftpd/virtusers.db

chmod 600 /etc/vsftpd/virtusers.db #设定PAM验证文件，并指定对虚拟用户数据库文件进行读取

七、在/etc/pam.d/vsftpd的文件头部加入以下信息（在后面加入无效）

修改前先备份 cp /etc/pam.d/vsftpd /etc/pam.d/vsftpdbak

vi /etc/pam.d/vsftpd

auth sufficient /lib64/security/pam_userdb.so db=/etc/vsftpd/virtusers

account sufficient /lib64/security/pam_userdb.so db=/etc/vsftpd/virtusers

注意：如果系统为32位，上面改为lib，否则配置失败

八、新建系统用户vsftpd，用户目录为/home/wwwroot, 用户登录终端设为/bin/false(即使之不能登录系统)

useradd vsftpd -d /home/wwwroot -s /bin/false

chown vsftpd:vsftpd /home/wwwroot -R

chown www:www /home/wwwroot -R #如果虚拟用户的宿主用户为www，需要这样设置。

九、建立虚拟用户个人Vsftp的配置文件

mkdir /etc/vsftpd/vconf

cd /etc/vsftpd/vconf

touch web1 web2 web3 #这里创建三个虚拟用户配置文件

mkdir -p /home/wwwroot/web1/http/

vi web1 #编辑用户web1配置文件，其他的跟这个配置文件类似
----------------------------------
local_root=/home/wwwroot/web1/http/
write_enable=YES
anon_world_readable_only=NO
anon_upload_enable=YES
anon_mkdir_write_enable=YES
anon_other_write_enable=YES
------------------------------------------
十、最后重启vsftpd服务器

systemctl restart vsftpd.service

备注：

guest_username=vsftpd #指定虚拟用户的宿主用户（就是我们前面新建的用户）

guest_username=www #如果ftp目录是指向网站根目录，用来上传网站程序，可以指定虚拟用户的宿主用户为nginx运行账户www，可以避免很多权限设置问题

至此，CentOS 7.0安装配置Vsftp服务器配置完成。







