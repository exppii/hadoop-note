CentOS6.5 x64 部署大数据集群运行环境
===

# 一、硬件环境

### 1. 集群硬件

|No.|CPU|RAM|HDD|
|:---:|:---|:---:|:---|
|PC1|i7 4770 3.4G 4core8thread |24G DDR3 1600MHz|2TB 7200rpm|
|PC2|i7 4770 3.4G 4core8thread |24G DDR3 1600MHz|2TB 7200rpm|
|PC3|i7 4770 3.4G 4core8thread |24G DDR3 1600MHz|2TB 7200rpm|
|PC4|i5 760 2.8G 2core4thread|4G DDR2 800MHz|1TB 7200rpm|
|PC5|Intel Dual-Core E7400@2.8GHz|4G DDR2 800MHz|320GB 7200rpm|
|PC6|Pentium Dual-Core E5200@2.5GHz|4G DDR2 800MHz|320GB 7200rpm|
|PC7|Pentium Dual-Core E5200@2.5GHz|2G DDR2 800MHz|250GB 7200rpm|
### 2.系统构架图
==暂缺==

### 3. 资源分配和拓扑
系统硬件包括7台PC。如下图所示，其中PC1～PC3作为集群三个**slave**，PC4 则为**Client**同时也是内部时钟同步服务器；PC5～PC6为zookeeper和master. slave是已虚拟机方式部署在三台已经部署了EXSi的PC机中。以slave1为例：slave1 所在PC4 IP地址为192.168.21.213. 但slave1系统实际地址为 192.168.21.201. 最新 Intel i7 ＋ z97 的EXSi安装参考附录1.



![network topology](../images/hardware_topology.png)
# 二、环境准备
### 1. 系统安装
PC4～PC7直接安装，PC1～PC3虚拟机配置如下：

|-|CPU|MEM|DISK|
|---|---|---|---|
|---|8core|24G|1.5TB|
在虚拟机里安装Linux系统（CentOS6.5 x86_64）采用自定义分区方式，分区信息如下：
![Custem_Partition](../images/Custem_Partition.png)
### 2.网络配置

更改**hostname**：可以运行命令行`hostname slave3.dream`零时修改，要永久更改则需编辑文件文件:
**/etc/sysconfig/network**

```apacheconf
NETWORKING=yes
HOSTNAME=slave3.dream
GATEWAY=192.168.21.254
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
参考**附录3** 同步服务器为 **client.dream(ip: 192.168.21.200)**

<!--同步配置参考文件: **appendix_2_NTP_Server_Setting.md**-->

### 10. 集群相关软件

各个版本软件下载地址

* Sun jdk8 | [Downloads]()
* Hadoop 2.3.0 | [Downloads](http://mirrors.cnnic.cn/apache/hadoop/common/hadoop-2.3.0/hadoop-2.3.0-src.tar.gz)
* HBase 0.98.5 | [Downloads](http://mirror.esocc.com/apache/hbase/hbase-0.98.5/hbase-0.98.5-hadoop2-bin.tar.gz)
* Zookeeper 3.4.6 | [Downloads](http://mirror.bit.edu.cn/apache/zookeeper/zookeeper-3.4.6/zookeeper-3.4.6.tar.gz)
* Phoenix 4.2.2 | [Downloads]()
* Kafka 0.8.1.1 | [Downloads]()
* ElasticSearch1.4.2 | [Downloads]()
* ~~Ganglia |[Downloads]()~~

解压安装(这里指定位置`/home/dream/Apps`),Hadoop为例：

```bash
tar -xf hadoop-2.3.0.tar.gz /opt/
chown -R dream:dream /opt/hadoop-2.3.0 /*更改权限*/
```
解压完之后，可删除原文件以节省空间。

### 11. LVM配置
参考 **附录4** 将逻辑卷挂载至目录：**/home/dream/Data** ==**并更改操作权限**==

```bash
chown -R dream:dream /home/dream/Data
chmod 775 /home/dream/Data
```

<!--同步配置参考文件: **appendix_3_LVM_Config.md**--> 

# 三、配置

### 1. 添加系统路径
修改配置文件**/etc/profile**, 运行命令使之生效`source /etc/profile`:

```apacheconf
#set java path
JAVA_HOME=/home/dream/Apps/jdk1.8.0_25
PATH=$PATH:$JAVA_HOME/bin
CLASSPATH=.:$JAVA_HOME/lib
export JAVA_HOME CLASSPATH

#set hadoop path
export HADOOP_HOME=/home/dream/Apps/hadoop-2.3.0
PATH=$PATH:$HADOOP_HOME/bin

#set hbase path
export HBASE_HOME=/home/dream/Apps/hbase-0.98.5
PATH=$PATH:$HBASE_HOME/bin

#set zookeeper path
#export ZOOKEEPER_HOME=/home/dream/Apps/zookeeper-3.4.6
#PATH=$PATH:$ZOOKEEPER_HOME/bin

export PATH
```

### 2. 提高文件打开上限
编辑文件**/etc/security/limits.conf**和 **/etc/security/limits.d/90-nproc.conf**在结尾加上：

```apacheconf
*          soft     nproc          65535
*          hard     nproc          65535
*          soft     nofile         65535
*          hard     nofile         65535
```

编辑文件**/etc/sysctl.conf**，在结尾加上:`fs.file-max = 65536`。重登录后执行`ulimit -a`验证：

```bash
[root@slave2 dream]# ulimit -a
core file size          (blocks, -c) 0
data seg size           (kbytes, -d) unlimited
scheduling priority             (-e) 0
file size               (blocks, -f) unlimited
pending signals                 (-i) 189590
max locked memory       (kbytes, -l) 64
max memory size         (kbytes, -m) unlimited
open files                      (-n) 65535
pipe size            (512 bytes, -p) 8
POSIX message queues     (bytes, -q) 819200
real-time priority              (-r) 0
stack size              (kbytes, -s) 10240
cpu time               (seconds, -t) unlimited
max user processes              (-u) 65535
virtual memory          (kbytes, -v) unlimited
file locks                      (-x) unlimited
[root@slave2 dream]# 
```

### 3. 集群软件配置

##### a). Hadoop 配置
**core-site.xml**:

```xml
<configuration>
  	<property>
    	<name>fs.defaultFS</name>
		<value>hdfs://hdpmaster.dream:9000</value>
		<description>hdfs 地址以及端口</description>
	</property>
 	<property>
    	<name>hadoop.tmp.dir</name>
    	<value>/home/dream/Data/hadoop-temp</value>
    	<description>hdfs 存储目录</description>
  	</property>
 	<property>
        <name>io.compression.codecs</name>
        <value>org.apache.hadoop.io.compress.SnappyCodec</value>
        <description>hdfs 数据压缩算法 必须手动编译</description>
	</property>    
</configuration>
```
**hdfs-site.xml**:

```xml
<configuration>
  	<property>
    	<name>dfs.replication</name>
    	<value>3</value>
    	<description>hdfs复制份数</description>
  	</property>
  	<property>
    	<name>dfs.datanode.max.xcievers</name>
    	<value>4096</value>
    	<description>最大链接数</description>
  	</property>
</configuration>
```
**mapred-site.xml**:

```xml
<configuration>
  	<property>
    	<name>mapreduce.framework.name</name>
    	<value>yarn</value>
    	<description>map-reduce运行框架 yarn：分布式模式</description>
  	</property>
</configuration>
```
**yarn-site.xml**:

```xml
<configuration>
  	<property>
　　		<name>yarn.resourcemanager.address</name>
　　		<value>hdpmaster.dream:8032</value>
  	</property>
  	<property>
　　		<name>yarn.resourcemanager.scheduler.address</name>
　　		<value>hdpmaster.dream:8030</value>
  	</property>
  	<property>
　　		<name>yarn.resourcemanager.resource-tracker.address</name>
　　		<value>hdpmaster.dream:8031</value>
  	</property>
  	<property>
　　		<name>yarn.resourcemanager.admin.address</name>
　　		<value>hdpmaster.dream:8033</value>
  	</property>
  	<property>
　　		<name>yarn.resourcemanager.webapp.address</name>
　　		<value>hdpmaster.dream:8088</value>
  	</property>
  	<property>
    	<name>yarn.nodemanager.aux-services</name>
    	<value>mapreduce_shuffle</value>
  	</property>
  	<property>
    	<name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
    	<value>org.apache.hadoop.mapred.ShuffleHandler</value>
  	</property>
</configuration>
```
**hadoop-env.sh**:

```bash
export JAVA_HOME=/home/dream/Apps/jdk1.8.0_25
export HADOOP_HEAPSIZE=4000
export HADOOP_COMMON_LIB_NATIVE_DIR="/home/dream/Apps/hadoop-2.3.0/lib/native/"
export HADOOP_OPTS="$HADOOP_OPTS -Djava.library.path=/home/dream/Apps/hadoop-2.3.0/lib/native/"
```
**yarn-env.sh**:

```bash
export JAVA_HOME=/home/dream/Apps/jdk1.8.0_25
JAVA_HEAP_MAX=-Xmx1000m
YARN_HEAPSIZE=4000
```
**slaves**:

```text
slave1.dream
slave2.dream
slave3.dream
```
##### b). HBase配置
拷贝**phoenix-4.2.2-bin**目录下所有 `jar`包拷贝至`$HBAE_HOME/lib`下：

```bash
cp $PHOENIX_HOME/*.jar $HBAE_HOME/lib/
```

在`$HBAE_HOME/lib`目录下创建文件夹`native/Linux-amd64-64`, 并拷贝`$HADOOP_HOME/lib/native/`下文件到此文件夹：

```bash
mkdir -p $HBAE_HOME/lib/native/Linux-amd64-64
cp $HADOOP_HOME/lib/native/* $HBAE_HOME/lib/native/Linux-amd64-64
```
**hbase-site.xml**:

```xml
<configuration>
  	<property>
    	<name>hbase.rootdir</name>
		<value>hdfs://hdpmaster.dream:9000/hbase</value>
	</property>
  	<property>
    	<name>hbase.cluster.distributed</name>
    	<value>true</value>
  	</property>
	<property>
    	<name>hbase.zookeeper.quorum</name>
    	<value>hdpmaster.dream,hbmaster.dream,dnsserver.dream</value>
  	</property>
	<property>
    	<name>hbase.zookeeper.property.dataDir</name>
		<value>/home/dream/Data/zookeeper</value>
	</property>
  	<property>
    	<name>hbase.server.thread.wakefrequency</name>
    	<value>1000</value>
  	</property>
	<property>
    	<name>zookeeper.session.timeout</name>
    	<value>360000</value>
  	</property>
	<property>
		<name>hbase.regionserver.global.memstore.lowerLimit</name>
    	<value>0.35</value>
  	</property>
	<property>
    	<name>hbase.hstore.blockingStoreFiles</name>
    	<value>100</value>
  	</property>
	<property>
    	<name>hbase.hstore.memstore.chunkpool.maxsize</name>
    	<value>0.5</value>
  	</property>
	<property>
    	<name>hbase.regionserver.dns.nameserver</name>
    	<value>192.168.21.211</value>
  	</property>
</configuration>
```
**hbase-env.sh**:

```bash
export JAVA_HOME=/home/dream/Apps/jdk1.8.0_25
export HBASE_LIBRARY_PATH=/home/dream/Apps/hbase-0.98.5/lib/native/Linux-amd64-64
export HBASE_HEAPSIZE=6000
export HBASE_OPTS="-XX:+UseParNewGC -XX:+UseConcMarkSweepGC -XX:CMSInitiatingOccupancyFraction=60 -XX:MaxTenuringThreshold=3"
export HBASE_MANAGES_ZK=false
export HADOOP_CONF_DIR=/home/dream/Apps/hadoop-2.3.0/etc/hadoop
```
**resgionserver**:

```text
slave1.dream
slave2.dream
slave3.dream
```
---
==zookeeper配置只安装在三个zookeeper master上 参考网络拓扑图，slave上不做配置==
##### c). Zookeeper配置

编辑文件**$ZOOKEEPER_HOME/conf/zoo.cfg** (`cp zoo.cfg.template zoo.cfg`)

```bash
udataDir=/home/dream/Data/zookeeper
maxClientCnxns=100
server.1=dnsserver.dream:2888:3888
server.2=hdpmaster.dream:2888:3888
server.3=hbmaster.dream:2888:3888 
```
在每个系统上（包含zookeeper）执行下面操作其中数字对应上面配置即 dnsserver->1, hdpmaster –>2 ：

```bash
mkdir –p /home/dream/Data/zookeeper
echo "1" > /home/dream/Data/zookeeper/myid
```
---
##### d). Kafka配置
编辑配置文件 **$KAFKA_HOME/config/server.properties** 

```bash
broker.id=3 # broker.id 
port=9092 # 端口
log.dirs=/home/dream/Data/kafka-logs #数据存储目录
# The minimum age of a log file to be eligible for deletion
log.retention.hours=1    #清除1hr之前的数据
# segments don't drop below log.retention.bytes.
log.retention.bytes=4294967296    #4G
# The maximum size of a log segment file. When this size is reached a new log 
# segment will be created.
log.segment.bytes=536870912       #512M
# The interval at which log segments are checked to see if they can be deleted
# according to the retention policies
log.retention.check.interval.ms=60000   #1 minute

zookeeper.connect=hdpmaster.dream:2181,hbmaster.dream:2181,dnsserver.dream:2181
# Timeout in ms for connecting to zookeeper
zookeeper.connection.timeout.ms=1000000
```

##### e). ElasticSearch 配置

安装 Elasticsearch JDBC 插件

```bash
$ELS_HOME/bin/plugin --install jdbc --url http://xbib.org/repository/org/xbib/elasticsearch/plugin/elasticsearch-river-jdbc/1.4.0.8/elasticsearch-river-jdbc-1.4.0.8-plugin.zip
```
==参考 附录5 修改Elasticsearch JDBC 插件==

拷贝 Phoenix JDBC driver到Elasticsearch plugins 目录：

```bash
cp $PHOENIX_HOME/phoenix-4.2.2-client.jar $ELS_HOME/plugins/jdbc/ 
```
更改 Elasticsearch 配置文件 **$ELS_HOME/config/elasticsearch.yml**:

```yaml
cluster.name: dream
node.name: "slave1"
```


### 4. 角色配置
##### a). 导出slave3作为模版(hadoop_slave.ova)
>在vSphere Client中部署ovf模板系统的MAC地址会变化。重新部署linux 的network后提示：device eth0 does not seem to be present, delaying initialization 解决方法如下：

* 运行`vim /etc/sysconfig/network-scripts/ifcfg-eth0`删掉原来有mac地址和uuid两行；
* 运行`vim /etc/udev/rules.d/70-persistent-net.rules`删除原来绑定mac地址行（所有）；
* 关机，使用vSphere Client

##### b). 使用模版分别创建slave1 和slave2
##### c). 修改文件/etc/sysconfig/network-scripts/ifcfg-eth0中对应IP地址
##### d). 更改hostname为对应hostname
##### e). Kafka配置文件中broker.id设置成对应ID编号
##### f). Elasticsearch配置文件中 node.name 设置成对应名称
##### g). ssh免密码登录
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


# 四、启动
### 1.Hadoop启动/关闭
在hdpmaster上使用普通用户（dream）先讲公钥拷贝到每一台slave上。同时，第一次启动必须先格式化namenode：

```bash
[dream@hdpmaster ~]$ hdfs namenode -format dream
15/01/22 17:17:47 INFO namenode.NameNode: STARTUP_MSG: 
/************************************************************
STARTUP_MSG: Starting NameNode
STARTUP_MSG:   host = hdpmaster.dream/192.168.21.213
STARTUP_MSG:   args = [-format, dream]
STARTUP_MSG:   version = 2.3.0
.....
15/01/22 17:17:50 INFO util.ExitUtil: Exiting with status 0
15/01/22 17:17:50 INFO namenode.NameNode: SHUTDOWN_MSG: 
/************************************************************
SHUTDOWN_MSG: Shutting down NameNode at hdpmaster.dream/192.168.21.213
************************************************************/
```
如上则表示格式成功，启动hdfs：

```bash
cd /home/dream/hadoop-2.3.0
sbin/start-dfs.sh 
```
使用`jps`查看hdpmaster上当前运行java线程

```bash
[dream@hdpmaster hadoop-2.3.0]$ jps
1824 NameNode
2128 Jps
2003 SecondaryNameNode
[dream@hdpmaster hadoop-2.3.0]$
```
查看slave上当前运行java线程

```bash
[dream@slave3 ~]$ jps
1490 DataNode
1657 Jps
[dream@slave3 ~]$
```
关闭**hdfs**则使用命令`sbin/stop-dfs.sh`。

### Yarn启动/关闭
同样是位于hdpmaster上执行：

```bash
cd /home/dream/hadoop-2.3.0
sbin/start-yarn.sh 
...
sbin/stop-yarn.sh
```
### Zookeeper启动/关闭
zookeeper需要登录到每一台zookeeper server上启动

```bash
ssh dream@dnsserver "/home/dream/Apps/zookeeper-3.4.6/bin/zkServer.sh start"
...
ssh dream@dnsserver "/home/dream/Apps/zookeeper-3.4.6/bin/zkServer.sh stop"
```
### HBase启动/关闭
登录hbmaster 执行：

```bash
start-hbase.sh
...
stop-hbase.sh
```
### Kafka启动/关闭
kafka server 需要登录至每一台slave上启动

```bash
[dream@slave1 kafka_2.9.2-0.8.1.1]$ nohup bin/kafka-server-start.sh config/server.properties &
[1] 1766
[dream@slave1 kafka_2.9.2-0.8.1.1]$ nohup: 忽略输入并把输出追加到"nohup.out"
...
[dream@slave1 kafka_2.9.2-0.8.1.1]$ bin/kafka-server-stop.sh config/server.properties
```

### ElasticSearch开启/关闭

ElasticSearch 需要登录至每一台slave上启动

```bash
[dream@slave2 Apps]$ cd elasticsearch-1.4.2/
[dream@slave2 elasticsearch-1.4.2]$ bin/elasticsearch &
```
查看是否成功启动

```bash
liuyoudeMacbook-Air:~ liuyou$ curl -X GET http://slave2.dream:9200
{
  "status" : 200,
  "name" : "slave2.dream",
  "cluster_name" : "dream",
  "version" : {
    "number" : "1.4.2",
    "build_hash" : "927caff6f05403e936c20bf4529f144f0c89fd8c",
    "build_timestamp" : "2014-12-16T14:11:12Z",
    "build_snapshot" : false,
    "lucene_version" : "4.10.2"
  },
  "tagline" : "You Know, for Search"
}
liuyoudeMacbook-Air:~ liuyou$
```

==以下操作**只需要在其中一台slave上执行**==

---
添加索引

```bash
curl -XPUT 'slave1.dream:9200/_river/phoenix_jdbc_river/_meta' -d '{
	"flush_interval" : "5s",
    "type" : "jdbc",
    "schedule" : "0/20 0-59 0-23 ? * *",
    "jdbc" : {
        "url" : "jdbc:phoenix:dnsserver.dream",
        "user" : "",
        "password" : "",
        "sql" : "select * from EVENT_LOG"
       }
}'
```
删除索引

```bash
curl -XDELETE 'slave1.dream:9200/_river/phoenix_jdbc_river'
```
---

# 五、错误处理

# 六、附录

## 附录1 EXSi5.5.ISO 添加Intel i218-v网卡驱动
ESXi5.5 本身并为支持最新Intel 9系芯片网卡驱动程序。为了让EXSi5.5在ASUS z97上正常运行，需要自行倒入相关驱动程序。

### 环境准备
* PowerShell 2.0或更高版本（Windows 7/8/8.1)
* [VMware vSphere PowerCLI](https://communities.vmware.com/community/vmtn/automationtools/powercli)
* [ESXi-Customizer-PS](http://vibsdepot.v-front.de/tools/ESXi-Customizer-PS-v2.3.ps1)
* [ESXi 5.5 Update 2 Offline Bundle](https://my.vmware.com/group/vmware/details?downloadGroup=ESXI55U2&productId=353&rPId=6656#) (替代EXSi5.5 ISO镜像)

### 驱动和链接

* [sata-xahci-1.24-1-offline_bundle.zip](http://vibsdepot.v-front.de/wiki/index.php/Sata-xahci) – addonboard SATA AHCI controller mappings
* [igb-5.2.7-1331820-offline_bundle-2157967.zip](https://my.vmware.com/group/vmware/details?downloadGroup=DT-ESXI55-INTEL-IGB-527&productId=353) – Intel igb 5.2.7 NIC driver
* [net-e1000e-3.1.0.2-glr-offline_bundle.zip](http://vibsdepot.v-front.de/wiki/index.php/Net-e1000e) – Intel e1000e 3.1.0.2 NIC driver


### 执行ESXi-Customizer-PS 批处理

第一次运行VMware vSphere PowerCLI 时可能会遇到无法加载 `*.ps1`的错误，这是因为操作系统默认禁止执行脚本，可以打开在管理员用下打开**powershell**，并执行：

```bash
Set-ExecutionPolicy remotesigned
```
新建离线驱动程序文件夹 **offline_bundles** 并将下载好的驱动文件拖至此文件夹。导航至ESXi-Customizer-PS目录，并在**PowerCLI**中运行如下命令：

```bash
.\ESXi-Customizer-PS-v2.3.ps1 
-pkgDir .\offline_bundles
-izip .\update-from-esxi5.5-5.5_update02-2068190.zip 
-nsc
```

如果编译成功，则由如下输出:

```bash
PowerCLI D:\> .\ESXi-Customizer-PS-v2.3.ps1 -pkgDir .\offline_bundles -iZip .\update-from-esxi5.5-5.5_update02-2068190.z
ip -nsc

Script to build a customized ESXi installation ISO or Offline bundle using the VMware PowerCLI ImageBuilder snapin
(Call with -help for instructions)

Logging to C:\Users\ADMINI~1\AppData\Local\Temp\ESXi-Customizer-PS.log ...

Running with PowerShell version 2.0 and VMware vSphere PowerCLI 5.8 Release 1 build 2057893

Adding base Offline bundle .\update-from-esxi5.5-5.5_update02-2068190.zip ... [OK]

Getting ImageProfiles, please wait ... [OK]

Using ImageProfile ESXi-5.5.0-20140902001-standard ...
(dated 08/23/2014 06:46:46, AcceptanceLevel: PartnerSupported,
For more information, see http://kb.vmware.com/kb/2079732.)

Loading Offline bundles and VIB files from .\offline_bundles ...
   Loading D:\offline_bundles\igb-5.2.7-1331820-offline_bundle-2157967.zip ... [OK]
      Add VIB net-igb 5.2.7-1OEM.550.0.0.1331820 [OK, replaced 5.0.5.1.1-1vmw.550.1.15.1623387]
   Loading D:\offline_bundles\net-e1000e-3.1.0.2-glr2-offline_bundle.zip ... [OK]
      Add VIB net-e1000e 3.1.0.2-glr2 [New AcceptanceLevel: CommunitySupported] [OK, replaced 1.1.2-4vmw.550.1.15.162338
7]
   Loading D:\offline_bundles\sata-xahci-1.27-1-offline_bundle.zip ... [OK]
      Add VIB sata-xahci 1.27-1 [OK, added]

Exporting the ImageProfile to 'D:\\ESXi-5.5.0-20140902001-standard-customized.iso'. Please be patient ...


All done.

PowerCLI D:\>
```
### 参考链接

* [Adding multiple drivers to an ESXi 5.5 u2 ISO](http://blog.kihltech.com/2014/10/adding-multiple-drivers-to-an-esxi-5-5-u2-iso/)
* [ESXi-Customizer-PS Instructions](http://www.v-front.de/p/esxi-customizer-ps.html#download)
## 附录2 DNS服务器配置
==空缺==
## 附录3 集群时钟同步配置（NTP）
目标环境，N台Linux CentOS6.5，一台作为NTP服务与外部NTP服务同步时间，同时，内网其他机器与这台
机器做时间同步。

|IP地址         |       角色      |       说明        |
|:------:      |       :---:     |         :---:    |
|192.168.21.200|    NTP 服务端   |  负责与外部服务器同步;<br> 为内外提供NTP服务 |
|192.168.21.XX |  内网NTP客户端   | 与192.168.21.200同步  |
| ******     |   内网NTP客户端      | 与192.168.21.200同步    |


### 下载安装同步服务
```bash
[root@client ~]# yum install ntp
```
在开启NTP服务前，先使用`ntpdate`命令直接同步（非平滑同步方式)，免得与外部时间相差太大
，让NTP不能正常同步:

```bash
[root@client ~]# ntpdate -u cn.pool.ntp.org
27 Dec 09:40:47 ntpdate[1971]: adjust time server 202.112.29.82 offset -0.078878 sec
```
### NTP Server端（192.168.21.200）配置
配置文件：**/etc/ntp.conf**

```apacheconf
# For more information about this file, see the man pages
# ntp.conf(5), ntp_acc(5), ntp_auth(5), ntp_clock(5), ntp_misc(5), ntp_mon(5).

driftfile /var/lib/ntp/drift

# 允许内网其他机器同步此机器
restrict 192.168.21.0 mask 255.255.255.0 nomodify notrap

# Use public servers from the pool.ntp.org project.
# Please consider joining the pool (http://www.pool.ntp.org/join.html).
#设置与中国相关服务器
server 210.72.145.44 perfer
server 1.cn.pool.ntp.org
server 0.asia.pool.ntp.org

#允许上层时间服务器 主动修改本机时间
restrict 1.cn.pool.ntp.org nomodify notrap noquery
restrict 0.asia.pool.ntp.org nomodify notrap noquery

#外部时间不可用时，以本地时间作为时间服务
server 127.127.1.0
fudge 127.127.1.0 stratum 10

includefile /etc/ntp/crypto/pw

# Key file containing the keys and key identifiers used when operating
# with symmetric key cryptography.
keys /etc/ntp/keys
# Specify the key identifiers which are trusted.
```
配置文件修改完成后保存退出，启动服务：

```bash
[root@client ~]# service ntpd start
```
启动后，一般需要5-10分钟才能与外部时间服务器同步时间。查看服务连接和监听：

```bash
[root@client ~]# netstat -tlunp | grep ntp
udp        0      0 192.168.21.200:123          0.0.0.0:*                               1130/ntpd
udp        0      0 127.0.0.1:123               0.0.0.0:*                               1130/ntpd
udp        0      0 0.0.0.0:123                 0.0.0.0:*                               1130/ntpd
udp        0      0 fe80::862b:2bff:fec0:fa5:123 :::*                                    1130/ntpd
udp        0      0 ::1:123                     :::*                                    1130/ntpd
udp        0      0 :::123                      :::*                                    1130/ntpd
[root@client ~]#

```
使用`ntpq -p`查看网路中NTP服务器，同时显示客户端和每个服务器都关系：

```bash
[root@client ~]# ntpq -p
remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
210.72.145.44   .INIT.          16 u    -  512    0    0.000    0.000   0.000
+gus.buptnet.edu 29.252.179.249   3 u   98  128  377   56.431   17.924  33.099
*time.iqnet.com  62.201.214.162   2 u   34  128  275  324.401   50.612  34.504
+dns.sjtu.edu.cn 15.179.156.248   3 u   69  128  377   36.576  -38.626  37.238
LOCAL(0)        .LOCL.          10 l  782   64    0    0.000    0.000   0.000
[root@client ~]#

```
OK,内网NTPD服务已经正常运行。添加开机启动：

```bash
[root@client ~]# chkconfig ntpd on
[root@client ~]# chkconfig --list ntpd
ntpd           	0:关闭	1:关闭	2:启用	3:启用	4:启用	5:启用	6:关闭
```
### NTP 内网Client端配置
为了简单，这里只列出了配置项，注释全部清理了。文件：**/etc/ntp.conf**

```apacheconf
# For more information about this file, see the man pages
# ntp.conf(5), ntp_acc(5), ntp_auth(5), ntp_clock(5), ntp_misc(5), ntp_mon(5).

driftfile /var/lib/ntp/drift

#允许上层时间服务器 主动修改本机时间
restrict default kod nomodify notrap nopeer noquery
restrict -6 default kod nomodify notrap nopeer noquery

restrict 127.0.0.1
restrict -6 ::1

#配置时间服务器地址
server client.dream
restrict client.dream nomodify notrap noquery

#外部时间不可用时，以本地时间作为时间服务
server 127.127.1.0
fudge 127.127.1.0 stratum 10
#end
```
保存退出后，先使用`ntpdate`手动同步下时间：

```bash
[root@slave1 ~]# ntpdate -u 192.168.21.200
```
然后启动服务，并添加开机启动（参考服务端启动命令）。
### 错误处理


### 参考链接
- [NTP服务及时间同步(CentOS6.x) - acooly](http://acooly.iteye.com/blog/1993484)
- [解决ntp的错误 no server suitable for synchronization found](http://blog.csdn.net/weidan1121/article/details/3953021)

## 附录4 Linux LVM 逻辑卷配置安装
### 1.系统安装部分
在虚拟机里安装Linux系统（CentOS6.5 x86_64 minimal）并预留分区给LVM卷：
![Custem_Partition](../images/Custem_Partition.png)
### 2.创建卷组
安装完成后，使用`fdisk －l`查看当前系统分区情况：

```bash
[root@slave3 ~]# fdisk -l

Disk /dev/sda: 1610.6 GB, 1610612736000 bytes
255 heads, 63 sectors/track, 195812 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x00020156

   Device Boot      Start         End      Blocks   Id  System
/dev/sda1   *           1          17      131072   83  Linux
Partition 1 does not end on cylinder boundary.
/dev/sda2              17        6544    52428800   83  Linux
/dev/sda3            6544      195813  1520303104   8e  Linux LVM
[root@slave3 ~]#
```
可以看到`/dev/sda3`已经是分区ID为**8e**（如果要新建LVM格式分区，参考后续扩容操作）。使用 `pvdisplay`查看当前物理卷：

```bash
[root@slave3 ~]# pvdisplay 
  "/dev/sda3" is a new physical volume of "1.42 TiB"
  --- NEW Physical volume ---
  PV Name               /dev/sda3
  VG Name               
  PV Size               1.42 TiB
  Allocatable           NO
  PE Size               0   
  Total PE              0
  Free PE               0
  Allocated PE          0
  PV UUID               9Or6xX-LiXG-4l40-hQBv-t7Uw-ZUfH-uKdJPR
   
[root@slave3 ~]#
```
创建卷组 **byonedata** ,并将刚才创建好的物理卷加入该卷组,命令为`vgcreate byonedata /dev/sda3`, 使用 `vgdisplay byonedata`查看:

```bash
[root@slave3 ~]# vgdisplay byonedata
  --- Volume group ---
  VG Name               byonedata
  System ID             
  Format                lvm2
  Metadata Areas        1
  Metadata Sequence No  1
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                0
  Open LV               0
  Max PV                0
  Cur PV                1
  Act PV                1
  VG Size               1.42 TiB
  PE Size               4.00 MiB
  Total PE              371167
  Alloc PE / Size       0 / 0   
  Free  PE / Size       371167 / 1.42 TiB
  VG UUID               oigueU-MUar-cJj9-NCzi-62q6-rInw-TV2Wl8
   
[root@slave3 ~]#
```
### 3. 创建逻辑卷
在创建好物理卷之后,就可以在物理卷组中添加逻辑卷了,创建逻辑卷的原则是“按需分配,动态调 整”,说的明白一点就是不要一次性将全部物理卷的空间分配给一个或者是几个逻辑卷,而是要根据 使用情况去动态的扩展使用的空间。

```bash
[root@slave3 ~]# lvcreate --name byonedataM --size 1T byonedata
  Logical volume "byonedataM" created
[root@slave3 ~]# 
```
使用`lvdisplay`查看逻辑卷：

```bash
[root@slave3 ~]# lvdisplay 
  --- Logical volume ---
  LV Path                /dev/byonedata/byonedataM
  LV Name                byonedataM
  VG Name                byonedata
  LV UUID                1PbqOy-bWfr-ACw2-ybcF-Bimu-eJtA-KuLcZD
  LV Write Access        read/write
  LV Creation host, time slave3.dream, 2015-01-22 10:17:05 +0800
  LV Status              available
  # open                 0
  LV Size                1.00 TiB
  Current LE             262144
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:0
   
[root@slave3 ~]# 
```
使用`mkfs.ext4`在逻辑卷**byonedataM**上创建**ext4**文件系统。

```bash
[root@slave3 ~]# mkfs.ext4 /dev/byonedata/byonedataM
mke2fs 1.41.12 (17-May-2010)
Filesystem label=
OS type:Linux
Block size=4096 (log=2)
Fragment size=4096 (log=2)
Stride=0 blocks, Stripe width=0 blocks
67108864 inodes, 268435456 blocks
13421772 blocks (5.00%) reserved for the super user
First data block=0
Maximum filesystem blocks=4294967296
8192 block groups
32768 blocks per group, 32768 fragments per group
8192 inodes per group
Superblock backups stored on blocks: 
	32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208, 
	4096000, 7962624, 11239424, 20480000, 23887872, 71663616, 78675968, 
	102400000, 214990848

Writing inode tables: done                            
Creating journal (32768 blocks): done
Writing superblocks and filesystem accounting information: done

This filesystem will be automatically checked every 24 mounts or
180 days, whichever comes first.  Use tune2fs -c or -i to override.
[root@slave3 ~]# 
```
将创建好的文件系统挂着至存储数据目录这里为 **/home/dream/Data**

```bash
[root@slave3 ~]# mount /dev/byonedata/byonedataM /home/dream/Data
[root@slave3 ~]# mount | grep /home/dream/Data
/dev/mapper/byonedata-byonedataM on /home/dream/Data type ext4 (rw)
[root@slave3 ~]# 
```
为了便于以后服务器重启自动挂载，需要将创建好的文件系统挂载信息添加到**/etc/fstab**里。UUID可以通过`blkid`命令查询

```bash
# /etc/fstab
# Created by anaconda on Wed Jan 21 09:59:02 2015
#
# Accessible filesystems, by reference, are maintained under '/dev/disk'
# See man pages fstab(5), findfs(8), mount(8) and/or blkid(8) for more info
#
UUID=5878b217-59c1-43c4-8f2f-bde2f3d5a67a /                       ext4    defaults        1 1
UUID=5b156431-3804-44f8-905b-141952481290 /boot                   ext4    defaults        1 2
tmpfs                   /dev/shm                tmpfs   defaults        0 0
devpts                  /dev/pts                devpts  gid=5,mode=620  0 0
sysfs                   /sys                    sysfs   defaults        0 0
proc                    /proc                   proc    defaults        0 0
UUID=a7292e64-914c-485c-b39a-56be8d3d2fe3 /home/dream/Data       ext4     defaults        0 0
```
查看**/etc/fstab**是否设置正确，先卸载逻辑卷，然后运行`mount －a`，使内核重新读取**/etc/fstab**. 看是否能够自动挂着：

```bash
[root@slave3 ~]# umount /home/dream/Data/
[root@slave3 ~]# mount -a
[root@slave3 ~]# mount | grep /home/dream/Data
/dev/mapper/byonedata-byonedataM on /home/dream/Data type ext4 (rw)
[root@slave3 ~]# 
```
### 4. 扩展逻辑卷
给逻辑卷增加空间并不会影响以前空间使用，所以无需卸载文件系统。直接通过命令 `lvextend -L +425G /dev/byonedata/byonedataM` 给 **byonedataM** 增加425GiB空间

```bash
[root@slave3 ~]# lvextend -L +425G /dev/byonedata/byonedataM
  Extending logical volume byonedataM to 1.42 TiB
  Logical volume byonedataM successfully resized
[root@slave3 ~]# lvs
  LV         VG        Attr       LSize Pool Origin Data%  Move Log Cpy%Sync Convert
  byonedataM byonedata -wi-ao---- 1.42t                                             
[root@slave3 ~]# 
```
扩展完成后使用`resize2fs`命令同步

```bash
resize2fs /dev/byonedata/byonedataM
```
### 5. 如何扩展卷组

==待续==

---
重新从新的磁盘中创建新分区sdb1，将分区ID转为**8e**。并将建好分区加入到已经存在的卷组**byonedata**中。通过 pvs查看命令是否成功。

```bash
vgextend byonedata /dev/sdb1
```
---
==待续==
## 附录5 自定义jdbc插件
elasticsearch-river-jdbc插件在更新最新数据时，对phoenix的sql支持有一些小问题。所以在此要更改其中文件org/xbib/elasticsearch/river/jdbc/strategy/simple/SimpleRiverSource.java 中几个地方

在SimpleRiverSource初始化的地方 加入变量 `g_iMaxCreateTime `:

```java
private static long g_iMaxCreateTime = 0;

   static {
       BufferedReader br =null;
       try {
           br = new BufferedReader(new FileReader("./LastCreateTime.dream"));
          String data = "",s ="";
          while ((data=br.readLine())!= null){
              s += data;
          }
           g_iMaxCreateTime = Long.valueOf(s);
           br.close();
       }catch (IOException e) {
          logger.debug("fuck file not exists.");
      }
   }
```
SimpleRiverSource.execute 添加如下：

```java
private void execute(SQLCommand command) throws Exception {
        Statement statement = null;
        ResultSet results = null;

        //only get new data add by byone
        String sql = command.getSQL() + " where CreateTime > " + g_iMaxCreateTime;
        logger.debug("fuck execute sql : {}", command.getSQL());
        //----------------add by byone----------------------
        command.setSQL(sql);
        try {
            if (command.isQuery()) {
                	...
                    merge(command, results, listener);

                    //write to file add by byone
                    logger.info("fuck maxcreatetime{}", g_iMaxCreateTime);
                    PrintWriter pw = new PrintWriter(new File("./LastCreateTime.dream"));
                    pw.write(String.valueOf(g_iMaxCreateTime));
                    pw.close();
                    //--------------add by byone -------------
                }
            } else {
                ...
                }
            }
        } finally {
            ...
        }
    }
```
SimpleRiverSource.processRow 添加如下：

```java
 private void processRow(ResultSet results, KeyValueStreamListener listener)
            throws SQLException, IOException {
        ...
        context.setLastRow(new HashMap());

        String strColName; //add by byone
        long iColValue; //add by byone
        for (int i = 1; i <= columns; i++) {
            try {
				...
                values.add(value);
                
                //update last createTime add by byone
                strColName = metadata.getColumnLabel(i);
                context.getLastRow().put("$row." + strColName, value);
                if (strColName.compareToIgnoreCase("CREATETIME") == 0)
                {
                    iColValue = Long.valueOf(value.toString());
                    if (iColValue > g_iMaxCreateTime)
                    {
                        g_iMaxCreateTime = iColValue;
                    }
                }
                //--------------add by byone-----------------

            } catch (ParseException e) {
                ...
            }
        }
        if (listener != null) {
            ...
        }
    }
```