### 1.初始准备：

- 准备3台虚拟机，其IP分别为：

```shell
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

三台机器在集群中所担任的角色：

- Master作为NameNode、ResourceManager、SecondaryNameNode
- Slave1作为DataNode、NodeManager
- Slave2也是作为DataNode、NodeManager

### 3.配置ssh免密码登录

三台机器分别运行指令生成密钥对，默认存放在`~/.ssh/`，设置默认回车：

```
ssh-keygen -t rsa　
```

在三个机器上，将公钥分别拷贝到其他机器：

```shell
ssh-copy-id -i ~/.ssh/id_rsa.pub Master #自身也要进行设置
ssh-copy-id -i ~/.ssh/id_rsa.pub Slave1
ssh-copy-id -i ~/.ssh/id_rsa.pub Slave2
```

拷贝成功后，测试免密登陆：

```shell
ssh Slave1
ssh Slave2
```

### 4.安装并配置Hadoop

若后续需要集成Hbase，需要注意此处的兼容性：<http://hbase.apache.org/book.html#hadoop>

在<http://mirror.bit.edu.cn/apache/>可以下载Apache有关的软件。

此处我们下载2.7.7版本：

```shell
cd /usr/local/
wget http://mirror.bit.edu.cn/apache/hadoop/common/hadoop-2.7.7/hadoop-2.7.7.tar.gz
tar -zxvf hadoop-2.7.7.tar.gz
rm hadoop-2.7.7.tar.gz
```

将Hadoop安装目录配置到环境变量中，方便后续使用：

```shell
vim ~/.bash_profile
# 添加以下内容
export HADOOP_HOME=/usr/local/hadoop-2.7.7/
export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH
```

安装成功后我们进行Hadoop的基本配置分别编辑`core-site.xml`以及`hdfs-site.xml`与`yarn-site.xml`的配置文件：

```shell
cd $HADOOP_HOME/etc/hadoop
vim core-site.xml  # 增加如下内容

<configuration>
    <property>
        <name>fs.default.name</name>
        <value>hdfs://Master:8020</value>  # 指定默认的访问地址以及端口号,设置Name Node所在地址
    </property>
</configuration>

vim hdfs-site.xml  # 增加如下内容

<configuration>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>/data/hadoop/app/tmp/dfs/name</value>  # namenode临时文件所存放的目录
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>/data/hadoop/app/tmp/dfs/data</value>  # datanode临时文件所存放的目录
    </property>
</configuration>

mkdir -p /data/hadoop/app/tmp/dfs/name
mkdir -p /data/hadoop/app/tmp/dfs/data

vim yarn-site.xml  # 增加如下内容

<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.resourcemanager.hostname</name>
        <value>Master</value>
    </property>
</configuration>
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.resourcemanager.hostname</name>
        <value>Master</value>
    </property>
</configuration>
```

拷贝并编辑MapReduce的配置文件：

```shell
cp mapred-site.xml.template mapred-site.xml
vim !$   # 增加如下内容

<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
</configuration>
```

配置从节点：

```shell
vim slaves

# 填入从节点的映射
Slave1
Slave2
```

接下来需要把Master上的Hadoop安装目录以及环境变量配置文件分发到其他两台机器上，在Master主机上分别执行如下命令：

```shell
rsync -av /usr/local/hadoop-2.7.7/ Slave1:/usr/local/hadoop-2.7.7/
rsync -av /usr/local/hadoop-2.7.7/ Slave2:/usr/local/hadoop-2.7.7/
rsync -av ~/.bash_profile Slave1:~/.bash_profile
rsync -av ~/.bash_profile Slave2:~/.bash_profile
```

到两台机器上分别执行source命令以及创建临时目录：

```shell
source ~/.bash_profile
mkdir -p /data/hadoop/app/tmp/dfs/name
mkdir -p /data/hadoop/app/tmp/dfs/data
```

### 5.格式化Hadoop并启停

在Master中对NameNode进行格式化操作：

```shell
hdfs namenode -format
```

启动集群：

```shell
start-dfs.sh
start-yarn.sh
```

查看进程：

```shell
jps  
# 查看是否有以下几个进程

# Master节点：
6256 Jps
5843 ResourceManager
5413 NameNode
5702 SecondaryNameNode

# Slave节点
6256 Jps
5538 DataNode
5945 NodeManager
```

访问监控主页：

在浏览器上访问主节点的50070端口：`192.168.42.128:50070`。可以访问50070端口就代表集群中的HDFS是正常的。

访问主节点的8088端口，这是YARN的web服务端口，例如：`192.168.42.128:8088`。

关闭节点：

```shell
stop-dfs.sh
stop-yarn.sh
```

