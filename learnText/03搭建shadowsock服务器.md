条件：pip
     yum install python-setuptools && easy_install pip 
-------------------------------------------------------------------------
安装：ssh
  # pip install shadowsocks

卸载已安装的package
  # pip uninstall shadowsocks

配置和使用
 1) vim创建该配置:
   vi /etc/ss_config.json

{
    "server":"107.182.176.112",
    "server_port":8980,
    "local_port":1080,
    "password":"wef3aaDewKe32s.sfw",
    "timeout":600,
    "method":"aes-256-cfb"
}
  2) 创建完毕后，赋予权限：
    chmod 755 /etc/ss_config.json
 
  3) 安装M2Crypto
	默认加密方法 table 速度很快，但很不安全。推荐使用 “aes-256-cfb” 或者 “bf-cfb”。请不要		使用 “rc4″，它不安全。如果选择 “table” 之外的加密，需要安装 M2Crypto。
	先安装依赖包：
	yum install -y openssl-devel gcc swig python-devel autoconf libtool安装setuptools：
	wget --no-check-certificate 			https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
	python ez_setup.py install再通过pip安装M2Crypto：
	pip install M2Crypto
   4) 安装 gevent
	安装 gevent可以提高 Shadowsocks 的性能。CentOS下安装gevent依赖libevent和greenlet。
	安装libevent：
	yum install -y libevent
	安装greenlet：
	pip install greenlet
	安装gevent：
	pip install gevent

    5) 命令行参数（服务器端启动命令）启动Shadowsocks
	ssserver -c /etc/ss_config.json
        ssserver -c /etc/ss_config.json -d start
        ssserver -c /etc/ss_config.json -d stop

    6) 如果想在后台一直运行Shadowsocks，启动命令如下：
        nohup ssserver -c /etc/config.json > /dev/null 2>&1 &

(备注：关于nohup，是可以让程序在后台运行的命令，当执行以上命令后，屏幕输出进程的pid，同时提示：
nohup: ignoring input and redirecting stderr to stdout
此时，再次回车一下，回到shell输入命令窗口即可。)


    7)开机自动启动
         vi /etc/rc.local

	在最后一行加上如下代码：
	/usr/bin/python /usr/bin/ssserver -c /etc/ss_config.json -d start

 

7)多用户配置：
{
    "server":"107.182.176.112",
    "server_port":8980,  
    "local_address": "127.0.0.1", 
    "local_port":1080,
    "port_password":{
         "8989":"password0",
         "9001":"password1",
         "9002":"password2",
         "9003":"password3",
         "9004":"password4"
    },
    "timeout":300,
    "method":"aes-256-cfb",
    "fast_open": false
}

   8)关掉firewalld.service，或打开相应端口。
     systemctl stop firewalld.service
     systemctl disablefirewalld.service



