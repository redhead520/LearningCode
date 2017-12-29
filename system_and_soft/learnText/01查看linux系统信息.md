
1 查看已安装的CentOS版本信息
   cat /proc/version
   uname -a

2. 查看linux版本：
  1) 列出所有版本信息: lsb_release -a 
  (注:这个命令适用于所有的linux，包括RedHat、SUSE、Debian等发行版。)
   2) 执行: cat /etc/issue
   3) 执行cat /etc/redhat-release (OK)
3.查看系统是64位还是32位:
    getconf LONG_BIT    
    file /bin/ls