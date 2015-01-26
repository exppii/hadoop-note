二、环境准备
===
### 1. 网络配置以及必要软件
更改**hostname**：可以运行命令行`hostname slave1.dream`零时修改，要永久更改则需编辑文件文件:
**/etc/sysconfig/network**

```vim
NETWORKING=yes
HOSTNAME=slave1.dream
GATEWAY=192.168.21.254
```
### 2. DNS域名服务器配置
参照附录5

### 3.配置DNS服务器地址

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

### 4. 防火墙配置

### 5. 更新系统

### 6. 下载软件
```bash
yum install java-1.8.0-openjdk-devel rsync vim
```

### 7. 配置时钟同步
更改时区：

```bash
cp /usr/share/zoneinfo/America/Chicago /etc/localtime
```
参考文件: **NTP\_Server\_Setting.md**

### 8. 添加统一访问用户
```bash
[root@localhost ~]# useradd example
[root@ localhost ~]# passwd example
Changing password for user example.
New UNIX password: 
Retype new UNIX password: 
passwd: all authentication tokens updated successfully.
[root@ localhost ~]#
```

### 9. 集群相关软件

各个版本软件下载地址

* Hadoop 2.3.0 | [Downloads](http://mirrors.cnnic.cn/apache/hadoop/common/hadoop-2.3.0/hadoop-2.3.0-src.tar.gz)
* HBase 0.98.5 | [Downloads](http://mirror.esocc.com/apache/hbase/hbase-0.98.5/hbase-0.98.5-hadoop2-bin.tar.gz)
* Zookeeper 3.4.6 | [Downloads](http://apache.fayea.com/apache-mirror/zookeeper/zookeeper-3.4.6/zookeeper-3.4.6.tar.gz)
* Phoenix 4.2.2 | [Downloads]()
* Kafka 0.8.1.1 | [Downloads]()
* ElasticSearch1.4.0 | [Downloads]()
* Ganglia |

解压安装(这里指定位置`/opt/`)以及同步至指定机器（参考部署图，以Hadoop为例）：

```bash
tar -xf hadoop-2.3.0.tar.gz /opt/
chown -R dream:dream /opt/hadoop-2.3.0 /*更改权限*/
```
rsync 同步代码参考 **hadoop_rsync.sh**

```bash
#!bin/bash
src="/opt/hadoop-2.3.0"
dests="slave1 slave2 slave3 hdpmaster client hbmaster"
dir="/opt/"
for des in $dests
do
    rsync –avhP –e ssh $src $des.dream:$dir
done
```
