# 二、环境准备
### 1. 系统安装
PC4～PC7直接安装，PC1～PC3虚拟机配置如下：

|-|CPU|MEM|DISK|
|---|---|---|---|
|---|8core|24G|1.5TB|
CentOS 7 系统默认文件系统为 XFS格式。

### 2.网络配置
**update:**
>centos7下 直接使用命令 `nmtui`进入ui界面设置hostname以及网络IP地址。

更改**hostname**：可以运行命令行`hostname slave3.dream`零时修改，要永久更改则需编辑文件文件:**/etc/hostname**

```bash
echo 'slave3.dream' > /etc/hostname
```

### 3.DNS服务器地址
这里默认使用`192.168.21.211` DNS服务器部署参照附录2。

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
yum install -y vim wget ntp unzip system-storage-manager rsync
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
### 6. 阻止远程root登录

修改sshd配置文件`vim /etc/ssh/sshd_config`, 添加如下:

```apacheconf
Port 22  #更改端口 默认为22
PermitRootLogin no #阻止远程root登录 默认为 yes
```
**update:**
> CentOS 7 废弃了iptables，而使用 `firewalld` 以及`firewalld-cmd` 命令。

~~如果修改了端口,则需要配置防火墙规则 `/etc/sysconfig/iptables`~~:

```apacheconf
-A INPUT -m state --state NEW -m tcp -p tcp --dport 9527 -j ACCEPT
```
重启服务

```bash
[root@ localhost ~]# systemctl restart sshd.service
[root@ localhost ~]# systemctl restart firewalld.service
```
### 7. 防火墙配置
==暂时先关闭==

```bash
[root@localhost ~]# systemctl disable firewalld
rm '/etc/systemd/system/dbus-org.fedoraproject.FirewallD1.service'
rm '/etc/systemd/system/basic.target.wants/firewalld.service'
[root@localhost ~]# systemctl stop firewalld
[root@localhost ~]# 
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
参考**附录3** 同步服务器为 **client.dream(ip: 192.168.21.200)**

<!--同步配置参考文件: **appendix_2_NTP_Server_Setting.md**-->

### 10. 集群相关软件

各个版本软件下载地址

* Sun jdk8 | [Downloads]()
* Hadoop 2.7.0 | [Downloads](http://mirrors.cnnic.cn/apache/hadoop/common/hadoop-2.7.0/hadoop-2.7.0-src.tar.gz)
* HBase 0.98.5 | [Downloads](http://mirror.esocc.com/apache/hbase/hbase-0.98.5/hbase-0.98.5-hadoop2-bin.tar.gz)
* Zookeeper 3.4.6 | [Downloads](http://mirror.bit.edu.cn/apache/zookeeper/zookeeper-3.4.6/zookeeper-3.4.6.tar.gz)
* Phoenix 4.2.2 | [Downloads]()
* Kafka 0.8.1.1 | [Downloads]()
* ElasticSearch1.4.2 | [Downloads]()
* ~~Ganglia |[Downloads]()~~

解压安装(这里指定位置`/home/dream/Apps`),Hadoop为例：

```bash
tar -xf hadoop-2.3.0.tar.gz /home/dream/Apps/
chown -R dream:dream /home/dream/Apps/hadoop-2.3.0 #更改权限
ln -s /home/dream/Apps/hadoop-2.3.0 /home/dream/Apps/hadoop
```
解压完之后，可删除原文件以节省空间。

###~~11. LVM配置~~
~~参考 **附录4** 将逻辑卷挂载至目录：**/home/dream/Data** ==**并更改操作权限**==~~

```bash
chown -R dream:dream /home/dream/Data
chmod 775 /home/dream/Data
```

<!--同步配置参考文件: **appendix_3_LVM_Config.md**--> 