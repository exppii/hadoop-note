# 三、配置

### 1. 添加系统路径
修改配置文件**/etc/profile**, 运行命令使之生效`source /etc/profile`:

```apacheconf
#set java path
JAVA_HOME=/home/dream/Apps/jdk8
PATH=$PATH:$JAVA_HOME/bin
CLASSPATH=.:$JAVA_HOME/lib
export JAVA_HOME CLASSPATH

#set hadoop path
export HADOOP_HOME=/home/dream/Apps/hadoop
PATH=$PATH:$HADOOP_HOME/bin

#set hbase path
export HBASE_HOME=/home/dream/Apps/hbase
PATH=$PATH:$HBASE_HOME/bin

#set zookeeper path
#export ZOOKEEPER_HOME=/home/dream/Apps/zookeeper
#PATH=$PATH:$ZOOKEEPER_HOME/bin

export PATH
```

### 2. Linux系统配置
提高文件打开上限,编辑文件**/etc/security/limits.conf**在结尾加上：

```apacheconf
*          -     nofile         65535
```
Linux内核配置，编辑文件**/etc/sysctl.conf**，在结尾加上:

```apacheconf
net.core.somaxconn = 4000
net.ipv4.tcp_fin_timeout = 20
net.ipv4.tcp_max_syn_backlog = 40000
net.ipv4.tcp_sack = 1
net.ipv4.tcp_timestamps = 0
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_window_scaling = 1
vm.swappiness = 0
fs.file-max = 65536
```
重登录后执行`ulimit -a`验证：

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
  	<property>
    <name>dfs.client.read.shortcircuit</name>
    <value>true</value>
  </property>
  <property>
    <name>dfs.domain.socket.path</name>
    <value>/var/lib/hadoop-hdfs/dn_socket</value>
    <description>mkdir /var/lib/hadoop-hdfs && chown -R dream:root /var/lib/hadoop-hdfs</description>
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
  	<property>
        <name>mapreduce.map.memory.mb</name>
        <value>2048</value>
    </property>
    <property>
        <name>mapreduce.reduce.memory.mb</name>
        <value>4096</value>
    </property>
    <property>
        <name>mapreduce.map.java.opts</name>
        <value>-Xmx1536m</value>
    </property>
    <property>
        <name>mapreduce.reduce.java.opts</name>
        <value>-Xmx3072m</value>
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
  	<property>
        <name>yarn.nodemanager.resource.memory-mb</name>
        <value>8192</value>
    </property>
    <property>
        <name>yarn.nodemanager.vmem-pmem-ratio</name>
        <value>8</value>
    </property>
    <property>
        <name>yarn.scheduler.maximum-allocation-mb</name>
        <value>8192</value>
    </property>
    <property>
        <name>yarn.scheduler.minimum-allocation-mb</name>
        <value>1024</value>
    </property>
</configuration>
```
**hadoop-env.sh**:

```bash
export HADOOP_SSH_OPTS="-p 8922"
export JAVA_HOME=/home/dream/Apps/jdk8
export HADOOP_HEAPSIZE=6000
export HADOOP_COMMON_LIB_NATIVE_DIR="/home/dream/Apps/hadoop/lib/native/"
export HADOOP_OPTS="$HADOOP_OPTS -Djava.library.path=/home/dream/Apps/hadoop/lib/native/"
```
**yarn-env.sh**:

```bash
export JAVA_HOME=/home/dream/Apps/jdk8
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
==**update:**==
> PHOENIX_HOME目录下`phoenix-4.2.2-client-without-hbase.jar`和`phoenix-4.2.2-client.jar`中和HBase本身log日志包冲突，应该删除掉。

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
export HBASE_SSH_OPTS="-p 8922"
export JAVA_HOME=/home/dream/Apps/jdk8
export HBASE_LIBRARY_PATH=/home/dream/Apps/hbase-0.98.5/lib/native/Linux-amd64-64
export HBASE_HEAPSIZE=6000
export HBASE_OPTS="-XX:+UseParNewGC -XX:+UseConcMarkSweepGC -XX:CMSInitiatingOccupancyFraction=60 -XX:MaxTenuringThreshold=3"
export HBASE_MANAGES_ZK=false
export HADOOP_CONF_DIR=/home/dream/Apps/hadoop/etc/hadoop
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
dataDir=/home/dream/Data/zookeeper
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
broker.id=2 # broker.id 
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
