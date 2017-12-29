本帖针对Centos6/REHL6系统
Gitlab的安装过程主要包括以下组件的配置:
	关闭selinux
	# 修改/etc/selinux/config 文件
	将SELINUX=enforcing改为SELINUX=disabled ,然后重启电脑
	# sestatus -v 查看selinux状态
	Current mode:                   permissive #说明已关闭selinux

	安装软件包及解决依赖项
	系统用户
	Ruby环境
	Go
	数据库(Mysql/Postgresql)
	Redis
	Gitlab-CE
	Nginx

1.安装软件包及解决依赖项
    添加EPEL源：

# 下载EPEL的GPG KEY，导入到系统中

wget -O /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-6 https://mirrors.tuna.tsinghua.edu.cn/epel/RPM-GPG-KEY-EPEL-6

rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-6

# 安装`epel-release-latest-6.noarch.rpm`包，启用EPEL

rpm -Uvh http://mirrors.ustc.edu.cn/epel/epel-release-latest-6.noarch.rpm

yum groupinstall "Development tools"
yum install gcc autoconf cmake unzip vim libcurl-devel zlib-devel curl-devel expat-devel gettext-devel openssl-devel perl-devel nodejs libicu-devel  wget curl

    node.js安装最新版：
1.下载已编译版本：
      wget https://nodejs.org/download/release/v6.2.1/node-v6.2.1-linux-x64.tar.gz
2.解压：
       sudo tar --strip-components 1 -xzvf node-v* -C /usr/local
3.老样子，测试安装：
	node --version

    git安装最新版

                1  curl -O --progress https://www.kernel.org/pub/software/scm/git/git-2.7.4.tar.gz
	        2  tar -xzf git-2.9.0.tar.gz
		   cd git-2.9.0
	        3  ./configure --prefix=/usr/local/git
		4   make prefix=/usr/local all
		    # 安装到/usr/local/bin
		5   make prefix=/usr/local install

                6  ln -s /usr/local/bin/git /usr/bin/
		   # 验证git版本号
		7  git --version
		    #查看git安装路径
		which git

		# 编辑 config/gitlab.yml (第5步中), 修改 git 路径为 /usr/local/bin/git
./configure --prefix=/usr/local/git
make
make install
git依赖  perl，cpio，zlib-devel，openssl-devel，expat-devel，gettext-devel这些包，如果出错基本上也是这些包造成的。 
0. Git安装前环境配置:
    $ yum install curl-devel expat-devel gettext-devel openssl-devel zlib-devel 
    $ apt-get install libcurl4-gnutls-dev libexpat1-dev gettext libz-dev libssl-dev 

$ sudo yum install libcurl4-openssl-dev

3. 编译源码：
   $ sudo make prefix=/usr/local/git all doc   // 这里同时指定all和doc这两个目标，指定doc是为了安装git的帮助文档到man手册里面，只指定all的话，默认并不包含git的帮助文档，这样在man手册中就查不到git的帮助。


5.安装数据库

   配置postgresql安装源：

# 修改/etc/yum.repos.d/CentOS-Base.repo,在[base]和[update]段落添加下面的配置
exclude=postgresql*
# 安装postgresql源
yum localinstall http://mirrors.ustc.edu.cn/postgresql/repos/yum/9.5/redhat/rhel-6-x86_64/pgdg-centos95-9.5-1.noarch.rpm
# 安装postgresql

初始化数据库
/usr/pgsql-9.5/bin/postgresql95-setup initdb  

 启动服务并设置为开机启动
systemctl enable postgresql-9.5  
systemctl start postgresql-9.5  
开放防火墙端口
firewall-cmd --permanent --add-port=5432/tcp  
firewall-cmd --permanent --add-port=80/tcp  
firewall-cmd --reload 
访问PostgreSQL
su - postgres 

CentOS7安装配置redis-3.0.0
#下载
wget http://download.redis.io/releases/redis-3.0.0.tar.gz
tar zxvf redis-3.0.0.tar.gz
cd redis-3.0.0
#如果不加参数,linux下会报错
make MALLOC=libc

 安装好之后,启动文件
#启动redis
src/redis-server &

#关闭redis
src/redis-cli shutdown
测试redis
清园
沉没的Atlantis

CentOS7安装配置redis-3.0.0

一.安装必要包

yum install gcc
二.linux下安装

#下载
wget http://download.redis.io/releases/redis-3.0.0.tar.gz
tar zxvf redis-3.0.0.tar.gz
cd redis-3.0.0
#如果不加参数,linux下会报错
make MALLOC=libc
 安装好之后,启动文件

#启动redis
src/redis-server &

#关闭redis
src/redis-cli shutdown
测试redis

$ src/redis-cli
127.0.0.1:6379> set foo bar
OK
127.0.0.1:6379> get foo
"bar"
$ 


sudo -u git -H bundle exec rake gitlab:shell:install[v2.0.1] REDIS_URL=unix:/var/run/redis/redis.sock RAILS_ENV=production


Gems in the groups development, test, mysql, aws, kerberos and postgres were not installed.


source "https://rubygems.org"

gem 'rails', '4.2.6'
gem 'rails-deprecated_sanitizer', '~> 1.0.3'

# Responders respond_to and respond_with
gem 'responders', '~> 2.0'

# Specify a sprockets version due to increased performance
# See https://gitlab.com/gitlab-org/gitlab-ce/issues/6069
gem 'sprockets', '~> 3.6.0'

# Default values for AR models
gem "default_value_for", "~> 3.0.0"

# Supported DBs
gem "mysql2", '~> 0.3.16', group: :mysql
gem "pg", '~> 0.18.2', group: :postgres












