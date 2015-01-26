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
#export ZOOKEEPER_HOME=/opt/zookeeper-3.4.6
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
		<value>hdfs://hdmaster.dream:9000</value>
		<description>hdfs 地址以及端口</description>
	</property>
 	<property>
    	<name>hadoop.tmp.dir</name>
    	<value>/home/dream/hadoop-temp</value>
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
		<value>hdfs://hdmaster.dream:9000/hbase</value>
	</property>
  	<property>
    	<name>hbase.cluster.distributed</name>
    	<value>true</value>
  	</property>
	<property>
    	<name>hbase.zookeeper.quorum</name>
    	<value>hdmaster.dream,hbmaster.dream,dnsserver.dream</value>
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
server.1=hbmaster.dream:2888:3888
server.2=hdmaster.dream:2888:3888
server.3=dnsserver.dream:2888:3888
```
在每个系统上（包含zookeeper）执行下面操作其中数字对应上面配置即 hbmaster->1, hdmaster –>2 ：

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
拷贝 Phoenix JDBC driver (==此处jar已被修改，参考附录4==)到Elasticsearch plugins 目录：

```bash
cp $PHOENIX_HOME/phoenix-4.2.2-client.jar $ELS_HOME/plugins/jdbc/ 
```
更改 Elasticsearch 配置文件 **$ELS_HOME/config/elasticsearch.yml**:

```yaml
cluster.name: dream
node.name: "slave1"
```
==以下操作推迟至生成EXSi模版之后执行，**只需要在其中一台slave上执行**==

---
添加索引

```bash
curl -XPUT 'slave1.dream:9200/_river/phoenix_jdbc_river/_meta' -d '{
	"flush_interval" : "5s",
    "type" : "jdbc",
    "schedule" : "0/10 0-59 0-23 ? * *",
    "jdbc" : {
        "url" : "jdbc:phoenix:hbmaster.dream",
        "user" : "",
        "password" : "",
        "sql" : "select * from EVENT_LOG"
       }
}'
```
---