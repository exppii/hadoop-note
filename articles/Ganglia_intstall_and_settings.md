Ganglia 安装
----
Ganglia 是 UC Berkeley 发起的一个开源监视项目，设计用于测量数以千计的节点。每台
计算机都运行一个收集和发送度量数据（如处理器速度、内存使用量等）的名为 gmond 的守护
进程。它将从操作系统和指定主机中收集。接收所有度量数据的主机可以显示这些数据并且可以
将这些数据的精简表单传递到层次结构中。正因为有这种层次结构模式，才使得 Ganglia 可
以实现良好的扩展。gmond 带来的系统负载非常少，这使得它成为在集群中各台计算机
上运行的一段代码，而不会影响用户性能。

### 1. Ganglia组件
Ganglia 监控套件包括三个主要部分：**gmond**，**gmetad**，和网页接口**ganglia-web**。
- **gmond**: 是一个守护进程，他运行在每一个需要监测的节点上，收集监测统计，发送和接受在同一个组
播或单播通道上的统计信息 如果他是一个发送者(mute=no)他会收集基本指标，比如系统负载（load_one）
,CPU利用率。他同时也会发送用户通过添加C/Python模块来自定义的指标。 如果他是一个接收者（deaf
=no）他会聚合所有从别的主机上发来的指标，并把它们都保存在内存缓冲区中。
- **gmetad**: 也是一个守护进程，他定期检查gmonds，从那里拉取数据，并将他们的指标存储在RRD
存储引擎中。他可以查询多个集群并聚合指标。他也被用于生成用户界面的web前端。
- **ganglia-web**:顾名思义，他应该安装在有gmetad运行的机器上，以便读取RRD文件。 集群是主机
和度量数据的逻辑分组，比如数据库服务器，网页服务器，生产，测试，QA等，他们都是完全分开的，你需要
为每个集群运行单独的gmond实例。

一般来说每个集群需要一个接收的gmond，每个网站需要一个gmetad

**Ganglia工作流如图所示:**
![ganglia data flow](../images/ganglia_data_flow.png)

左边是运行在各个节点上的gmond进程，这个进程的配置只由节点上/etc/gmond.conf的文件决定。所以，
在各个监视节点上都需要安装和配置该文件。右上角是更加负责的中心机（通常是这个集群中的一台，也可以
不是）。在这个台机器上运行这着gmetad进程，收集来自各个节点上的信息并存储在rrdtool上，该进程
的配置只由/etc/gmetad.conf决定。右下角显示了关于网页方面的一些信息。我们的浏览网站时调用php
脚本，从RRDTool数据库中抓取信息，动态的生成各类图表。
### 2. 安装必要依赖
切换至**root**用户:
```bash
[root@client ~]# yum install –y gcc gcc-c++ libpng freetype zlib libdbi apr* libxml2-devel pkg-config glib pixman pango pango-devel freetye-devel fontconfig cairo cairo-devel libart_lgpl libart_lgpl-devel pcre* rrdtool*
```
### 3. 安装expat并
```bash
[root@client ~]# cd /home/dream
[root@client ~]# wget http://jaist.dl.sourceforge.net/project/expat/expat/2.1.0/expat-2.1.0.tar.gz
[root@client ~]# tar -xf expat-2.1.0.tar.gz
[root@client ~]# cd expat-2.1.0
[root@client ~]# ./configure --prefix=/usr/local/expat
[root@client ~]# make -j4 && make install
```
对于64位操作系统，需要手动拷贝动态链接库到lib64下：
```bash
[root@client ~]# mkdir /usr/local/expat/lib64  
[root@client ~]# cp -a /usr/local/expat/lib/* /usr/local/expat/lib64/
```
### 4. 安装confuse并手动拷贝动态链接库到lib64下
### 5. 安装Ganlia
### 6. 服务端配置(gmetad节点)
### 7. 客户端配置(gmond节点)
### 8. Web服务配置
### 9. Ganglia监控HADOOP、HBASE配置选项
