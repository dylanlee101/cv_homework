### 1.初始准备：

- 准备3台虚拟机，其IP分别为：

```
192.168.42.128
192.168.42.129
192.168.42.130
```

- 需要安装好JDK，环境生效即可
- 需要配置好Hadoop并启动
- 配置好Zookeeper（可选）

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

三台机器在集群中所担任的角色：

- Master作为HMaster
- Slave1作为HRegionServer
- Slave2也是作为HRegionServer

### 3.安装配置Hbase

在<http://mirror.bit.edu.cn/apache/>可以下载Apache有关的软件。

此处我们下载2.1.5版本：

```shell
cd /usr/local
wget http://mirror.bit.edu.cn/apache/hbase/2.1.5/hbase-2.1.5-bin.tar.gz
tar -zxvf hbase-2.1.5-bin.tar.gz
rm hbase-2.1.5-bin.tar.gz
```

配置环境变量`vim ~/.bash_profile`:

```shell
export HADOOP_HOME=/usr/local/hadoop-2.7.7/
export ZOOKEEPER_HOME=/usr/local/zookeeper-3.4.14/
export HBASE_HOME=/usr/local/hbase-2.1.5
export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$ZOOKEEPER_HOME/bin:$HBASE_HOME/bin:$PATH
```

配置：

```
/usr/local/hbase/conf
```

配置hbase-env.sh:

```shell
vim hbase-env.sh
# 以下为内容
# 此配置信息，默认为true，使用Hbase默认的zookeeper。此处设置为false，使用独立的zookeeper
export HBASE_MANAGES_ZK=false
#Hbase日志目录
export HBASE_LOG_DIR=/usr/local/hbase-2.1.5/logs
```

配置 hbase-site.xml：

```shell
<configuration>
	<property>
		<name>hbase.rootdir</name>
		<value>hdfs://Master:9000/hbase</value>
	</property>
	## 设置为true使用完全分布式
	<property>
		<name>hbase.cluster.distributed</name>
		<value>true</value>
	</property>
	<property>
		<name>hbase.master</name>
		<value>Master:60000</value>
	</property>
	## zookeeper位置，使用默认Zookeeper可不配置
	<property>
		<name>hbase.zookeeper.quorum</name>
		<value>Master,Slave1,Slave2</value>
	</property>
</configuration>
```

配置regionservers：

```shell
cd $HBASE_HOME
vim conf/regionservers

# 添加regionservers的机器
Slave1
Slave2
```

复制hbase到其他两台机器：

```shell
rsync -av /usr/local/hbase-2.1.5/ Slave1:/usr/local/hbase-2.1.5/
rsync -av /usr/local/hbase-2.1.5/ Slave2:/usr/local/hbase-2.1.5/
```

在主节点上启动Hbase：

```shell
start-hbase.sh
```

使用jps：

```shell
## master中的HBase信息
5471 HMaster             # hbase master进程

## salve中的HBase信息
4143 HRegionServer        # hbase slave进程
```

访问web界面：http://localhost:16010

关闭Hbase：

```shell
stop-hbase.sh
```

debug指南：使用hbse hbck查看是否达到一致性，若无则查看错误信息与日志中的错误信息