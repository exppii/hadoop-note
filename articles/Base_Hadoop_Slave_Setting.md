


二、环境准备
===

### 1. 系统安装
虚拟机配置：

|-|CPU|MEM|DISK|
|---|---|---|---|
|---|8core|24G|1.5TB|
在虚拟机里安装Linux系统（CentOS6.5 x86_64 minimal）并预留分区给LVM卷：
![Custem_Partition](../images/Custem_Partition.png)
### 2.网络配置

更改**hostname**：可以运行命令行`hostname slave1.dream`零时修改，要永久更改则需编辑文件文件:
**/etc/sysconfig/network**

```apacheconf
NETWORKING=yes
HOSTNAME=slave1.dream
GATEWAY=192.168.21.254
```
### 3.DNS服务器地址
这里默认使用`192.168.21.211` DNS服务器部署参照附录1。

<!--同步配置参考文件: **DNS_Server_Setting.md**-->
```bash
echo 'nameserver 192.168.21.211' > /etc/resolv.conf
```
为了防止重启后文件**/etc/resolv.conf**内容配系统刷掉，还要执行：
>文件名字可能并非**ifcfg-eth0**,可`cd`至相应目录查看

```bash
echo "PEERDNS=no" >> /etc/sysconfig/network-scripts/ifcfg-eth0
```
如需连接外部网络可再往**/etc/resolv.conf** 中添加`8.8.8.8`:

```bash
echo 'nameserver 8.8.8.8' >> /etc/resolv.conf
```
### 4. 必要软件
```bash
yum install vim wget ntp unzip 
```
### 5. 添加统一普通Hadoop用户
添加统一访问用户

```bash
[root@localhost ~]# useradd example
[root@ localhost ~]# passwd example
Changing password for user example.
New UNIX password: 
Retype new UNIX password: 
passwd: all authentication tokens updated successfully.
[root@ localhost ~]#
```
==以下两步操作推迟至生成EXSi模版之后执行==

---
切换至普通用户生成`rsa key`对

```bash
[root@slave2 Downloads]# su dream
[dream@slave2 Downloads]$ ssh-keygen -t rsa -C "slave2.dream"
Generating public/private rsa key pair.
Enter file in which to save the key (/home/dream/.ssh/id_rsa): 
Created directory '/home/dream/.ssh'.
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/dream/.ssh/id_rsa.
Your public key has been saved in /home/dream/.ssh/id_rsa.pub.
The key fingerprint is:
0c:3d:17:f1:6b:a9:8b:a0:69:09:5c:f6:23:c3:49:64 slave2.dream
The key's randomart image is:
+--[ RSA 2048]----+
|          o.     |
|    E  .   o     |
|   o  . o . .    |
|    +  o o   o   |
| . = o  S   +    |
|  o = o    o     |
|   . +..  .      |
|    oo . . .     |
|   .o   . .      |
+-----------------+
[dream@slave2 Downloads]$ 
```
拷贝公钥到本机：

```bash
[dream@slave2 Downloads]$ ssh-copy-id -i ~/.ssh/id_rsa.pub localhost
The authenticity of host 'localhost (::1)' can't be established.
RSA key fingerprint is 5d:3b:5f:96:ff:8c:dc:52:be:9d:22:3d:f4:6b:bc:ad.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'localhost' (RSA) to the list of known hosts.
dream@localhost's password: 
Now try logging into the machine, with "ssh 'localhost'", and check in:

  .ssh/authorized_keys

to make sure we haven't added extra keys that you weren't expecting.

[dream@slave2 Downloads]$ 
```
----
==以上两步操作推迟至生成EXSi模版之后执行==
### 6. 阻止远程root登录

修改sshd配置文件`vim /etc/ssh/sshd_config`, 添加如下:

```apacheconf
Port 22  #更改端口 默认为22
PermitRootLogin no #阻止远程root登录 默认为 yes
```
如果修改了端口,则需要配置防火墙规则 `/etc/sysconfig/iptables`:

```apacheconf
-A INPUT -m state --state NEW -m tcp -p tcp --dport 9527 -j ACCEPT
```
重启服务

```bash
[root@ localhost ~]# service sshd restart
[root@ localhost ~]# service iptables restart
```
### 7. 防火墙配置
==暂时先关闭==

```bash
service iptables stop  #关闭防火墙
chkconfig iptables off #开机不启动
```
### 8. [可选]更新系统
==暂时未执行==

```bash
yum update
```
### 9. 配置时钟同步
如有必要，调整时区为 `亚洲/上海`：

```bash
cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
```
参考**附录2** 同步服务器为 **client.dream(ip: 192.168.21.200)**

<!--同步配置参考文件: **appendix_2_NTP_Server_Setting.md**-->

### 10. 集群相关软件

各个版本软件下载地址

* Sun jdk8 | [Downloads]()
* Hadoop 2.3.0 | [Downloads](http://mirrors.cnnic.cn/apache/hadoop/common/hadoop-2.3.0/hadoop-2.3.0-src.tar.gz)
* HBase 0.98.5 | [Downloads](http://mirror.esocc.com/apache/hbase/hbase-0.98.5/hbase-0.98.5-hadoop2-bin.tar.gz)
* Zookeeper 3.4.6 | [Downloads](http://apache.fayea.com/apache-mirror/zookeeper/zookeeper-3.4.6/zookeeper-3.4.6.tar.gz)
* Phoenix 4.2.2 | [Downloads]()
* Kafka 0.8.1.1 | [Downloads]()
* ElasticSearch1.4.2 | [Downloads]()
* ~~Ganglia |[Downloads]()~~

解压安装(这里指定位置`/home/dream/Apps`),Hadoop为例：

```bash
tar -xf hadoop-2.3.0.tar.gz /opt/
chown -R dream:dream /opt/hadoop-2.3.0 /*更改权限*/
```
### 11. LVM配置
参考 **附录3** 将逻辑卷挂载至目录：**/home/dream/Data**

<!--同步配置参考文件: **appendix_3_LVM_Config.md**--> 

