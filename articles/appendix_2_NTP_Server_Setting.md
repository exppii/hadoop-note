集群时钟同步配置（NTP）
===
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
server 192.168.21.200
restrict 192.168.21.200 nomodify notrap noquery

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
