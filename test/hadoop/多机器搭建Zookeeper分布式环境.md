### 1.初始准备：

- 准备3台虚拟机，其IP分别为：

```
192.168.42.128
192.168.42.129
192.168.42.130
```

- 需要安装好JDK，环境生效即可

### 2.配置IP映射

编辑`/etc/hosts`配置文件：

```shell
vim /etc/hosts  # 三台机器都需要操作

# 添加以下内容
192.168.42.128 Master
192.168.42.129 Slave1
192.168.42.130 Slave2

# 重启
reboot
```

三台机器都进行Zookeeper的设置。

### 3.安装配置Zookeeper

在<http://mirror.bit.edu.cn/apache/>可以下载Apache有关的软件。

此处我们下载3.4.14版本：

```shell
cd /usr/local
wget http://mirror.bit.edu.cn/apache/zookeeper/zookeeper-3.4.14/zookeeper-3.4.14.tar.gz
tar -zxvf zookeeper-3.4.14.tar.gz
rm zookeeper-3.4.14.tar.gz
```

设置配置文件`zoo.cfg`，将`zoo_sanple.cfg`改为`zoo.cfg`：

```shell
cd zookeeper-3.4.14
mv zoo_sample.cfg zoo.cfg
vim zoo.cfg
```

修改为以下信息：

```java
tickTime=2000
initLimit=10
syncLimit=5
dataDir=/var/zookeeper
clientPort=2181

server.1=Master:2888:3888
server.2=Slave1:2888:3888 
server.3=Slave2:2888:3888
```

在三个机器都创建数据目录：

```shell
mkdir -r /var/zookeeper
```

在`/var/zookeeper`中创建文件`myid`：

```shell
vim /var/zookeeper/myid
# 添加以下内容，此数字与zoo.cfg严格对应
# 在本例中，Master机器该文件中数字为1，Slave1机器中该文件数字为2，Slave2机器中该文件数字为3
1
```

在三个机器中将Zookeeper安装目录配置到环境变量中，方便后续使用：

```shell
vim ~/.bash_profile
# 改为以下内容
export HADOOP_HOME=/usr/local/hadoop-2.7.7/
export ZOOKEEPER_HOME=/usr/local/zookeeper-3.4.14/
export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$ZOOKEEPER_HOME/bin:$PATH
```

将Zookeeper文件传输到其余两台机器：

```shell
rsync -av /usr/local/zookeeper-3.4.14/ Slave1:/usr/local/zookeeper-3.4.14/
rsync -av /usr/local/zookeeper-3.4.14/ Slave2:/usr/local/zookeeper-3.4.14/
```

在每台机器中运行启动Zookeeper命令：

```shell
zkServer.sh start
```

启动后使用jsp会看到QuorumPeerMain进程，但并不代表一定启动成功。

```shell
jsp
```

查看Zookeeper状态：

```shell
zkServer.sh status
# 若成功会显示以下内容（分别有一个Leader与两个Follower） ：
ZooKeeper JMX enabled by default
Using config: /usr/local/zookeeper-3.4.14/bin/../conf/zoo.cfg
Mode: follower
```

如果出现问题，可以先关闭zookeeper，再使用foreground启动zookeeper进行调试，指令如下：

```shell
zkServer.sh start-foreground
```

