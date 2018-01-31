要使用systemctl命令。

  
------------------------------------------------------------------------
1。查看默认启动的服务：（如果不用grep过滤一下，输出结果有260多行）
 systemctl list-unit-files|grep enabled

2. 看看监听端口（command not found:yum install net-tools）
  netstat -lntp

3.启用sshd  (老命令： chkconfig sshd on)
  systemctl enable sshd.service 
  systemctl disable sshd.service
4.打开，关闭，重启sshd  （老命令：service sshd start）
   systemctl start sshd.service
   systemctl stop sshd.service
   systemctl restart sshd.servic

5.　写入配置文件
   打开iptables的配置文件：vi /etc/sysconfig/iptables
----------------------------------------------------------------------
解决ssh无操作自动断开
  1、终端键入：echo $TMOUT 
	 如果显示空白，表示没有设置，等于使用默认值0，一般情况下应该是不超时。如果大于0，可以在	如/etc/profile之类文件中设置它为0
  2、修改/etc/ssh/sshd_config文件（要sudo），
将ClientAliveInterval 0和ClientAliveCountMax 3的注释符号去掉，
然后将ClientAliveInterval的值0改成60，
ClientAliveCountMax的值3改成10000。
ClientAliveInterval指定了服务器端向客户端请求消息的时间间隔，默认是0，不发送。
而ClientAliveInterval 60表示每分钟发送一次，然后客户端响应，这样就保持长连接了。ClientAliveCountMax，使用默认值3即可，ClientAliveCountMax表示服务器发出请求后客户端没有响应的次数达到一定值，就自动断开，设成10000或更大，保证不断开（真没验证过。。。）


For Ubuntu 14.04 and 16.04 users, please install from PPA:

sudo apt-get install software-properties-common -y
sudo add-apt-repository ppa:max-c-lv/shadowsocks-libev -y
sudo apt-get update
sudo apt install shadowsocks-libev
配置文件
编辑 /etc/shadowsocks-libev/config.json
/etc/init.d/shadowsocks-libev start
