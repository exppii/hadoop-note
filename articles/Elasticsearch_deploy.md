Elasticsearch deploy
===

### 1. 准备:
- 下载 JDK and set JAVA_HOME
- 下载 HADOOP,HBase and deploy
- 下载 Phoenix and deploy

### 2. 下载安装 Elasticsearch
```bash
wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.4.2.tar.gz
tar -xf elasticsearch-1.4.2.tar.gz
```
安装 Elasticsearch JDBC 插件

```bash
$ELS_HOME/bin/plugin --install jdbc --url http://xbib.org/repository/org/xbib/elasticsearch/plugin/elasticsearch-river-jdbc/1.4.0.8/elasticsearch-river-jdbc-1.4.0.8-plugin.zip
```
拷贝 Phoenix JDBC driver 到Elasticsearch plugins 目录：

```bash
cp $PHOENIX_HOME/phoenix-4.2.2-client.jar $ELS_HOME/plugins/jdbc/ 
```
更改 Elasticsearch 配置文件 **$ELS_HOME/config/elasticsearch.yml**:

```yaml
cluster.name: dream

node.name: "slave1"
```

同步到其他节点:

```bash
rsync -avhP -e ssh elasticsearch-1.4.2 slave1:/home/dream/
```
启动：

```bash
nohup $ELS_HOME/bin/elasticsearch &
tail nohup.out
```
检查是否运行：

```bash
curl -X GET http://slave1.dream:9200
```
添加Driver：

```bash
curl -XPUT 'slave1.dream:9200/_river/phoenix_jdbc_river/_meta' -d '{
	"flush_interval" : "5s",
    "type" : "jdbc",
    "jdbc" : {
        "url" : "jdbc:phoenix:hbmaster.dream",
        "user" : " ",
        "password" : "",
        "sql" : [
            {
                "statement" : "select * from event_log where eventtype = ?",
                "parameter" : ["a19327fce0c8493c8f0db0605a1bdf52"]
            }
        ]
    }
}'

curl -XPUT 'slave3.dream:9200/_river/phoenix_jdbc_river/_meta' -d '{
	"flush_interval" : "5s",
    "type" : "jdbc",
    "jdbc" : {
        "url" : "jdbc:phoenix:hbmaster.dream",
        "user" : "",
        "password" : "",
        "sql" : [
            {
                "statement" : "select * from \"EVENT_LOG\" where \"createtime\" > ?",
                "parameter" : [ "$river.state.last_active_begin" ]
            }
        ],
        "index" : "dream_jdbc_river_index",
        "type" : "dream_jdbc_river_type"
    }
}'



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





"sql" : [
            {
                "statement" : "select * from EVENT_LOG > 1420707094596",
                "parameter" : [ "1" ]
            }
        ]


"schedule" : "0 0-59 0-23 ? * *",
curl -XDELETE 'slave1.dream:9200/_river/phoenix_jdbc_river'

curl -XPOST 'slave1.dream:9200/_river/_refresh'
```

