build hadoop2.7 in centos 7
===

### 安装依赖

系统方式安装

```bash
yum  install gcc gcc-c++ autoconf automake cmake libtool snappy-devel openssl-devel
```
额外的软件

* maven3.3 |[download](http://mirrors.cnnic.cn/apache/maven/maven-3/3.3.3/binaries/apache-maven-3.3.3-bin.tar.gz)
* sun-jdk1.8 | [download](http://mirrors.cnnic.cn/apache/hadoop/common/hadoop-2.7.0/hadoop-2.7.0-src.tar.gz)
* protobuf2.5.0 | [download](http://mirrors.cnnic.cn/apache/hadoop/common/hadoop-2.7.0/hadoop-2.7.0-src.tar.gz)
* hadoop2.7 src ｜[download](http://mirrors.cnnic.cn/apache/hadoop/common/hadoop-2.7.0/hadoop-2.7.0-src.tar.gz)

配置java以及maven路径 （这里将程序放置在 `/home/dream/Apps/`）:
在**/etc/profile** 结尾添加并运行命令 `source /etc/profile` 使之生效。

```apacheconf
#set java path
JAVA_HOME=/home/dream/Apps/jdk8
PATH=$PATH:$JAVA_HOME/bin
CLASSPATH=.:$JAVA_HOME/lib
export JAVA_HOME CLASSPATH

#set maven path
export MAVEN_HOME=/home/dream/Apps/maven
PATH=$PATH:$MAVEN_HOME/bin

export PATH
```

执行命令

```bash
mvn package -Pdist,native -DskipTests -Dtar -Drequire.snappy -X
```


