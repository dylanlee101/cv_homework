### 1.初始准备：

- 准备3台虚拟机，其IP分别为：

```
192.168.42.137
192.168.42.136
192.168.42.135
```

- 需要安装好JDK，环境生效即可
- 需要配置好Hadoop并启动
- 需要安装并配置好Mysql

### 2.安装Hive

在Hive2.x中已经将MapReduce设置为deprecated了，改为支持其他计算引擎（比如Spark）。在未来可能会彻底移除，如果想要主要使用MapReduce进行操作，建议使用低版本比如Hive1.x。

在Apache的官方镜像中我们可以下载Hive的各个版本：<https://mirrors.tuna.tsinghua.edu.cn/apache/hive/>

此处我们选择最新版Hive_2.3.6

首先下载Hive_2.3.6

```shell
cd /usr/local
wget https://mirrors.tuna.tsinghua.edu.cn/apache/hive/stable-2/apache-hive-2.3.6-bin.tar.gz
tar -zxvf apache-hive-2.3.6-bin.tar.gz
mv apache-hive-2.3.6-bin hive-2.3.6
```

修改环境变量：

```shell
vim ~/.bashrc

# 在尾部添加一下内容
export HIVE_HOME="/usr/local/hive-2.3.6"
export PATH=$PATH:$HIVE_HOME/bin

# 刷新配置
source ~/.bashrc
```

HIVE有三种运行模式，此处我们选择远程Mysql模式。设置Hive的核心配置：

```shell
vim /hive-2.3.6/conf/hive-site.xml

# 添加以下内容,IP(Master)改为主机IP
<?xml version="1.0" encoding="UTF-8" standalone="no"?><?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
        <property>
                <name>javax.jdo.option.ConnectionURL</name>
                <value>jdbc:mysql://Master:3306/hivedb?createDatabaseIfNotExist=true&amp;characterEncoding=UTF-8&amp;useSSL=false&amp;serverTimezone=UTC</value>
        </property>

        <property>
                <name>javax.jdo.option.ConnectionDriverName</name>
                <value>com.mysql.cj.jdbc.Driver</value>
        </property>

		## 你的Mysql账号
        <property>
                <name>javax.jdo.option.ConnectionUserName</name>
                <value>root</value>
        </property>

		## 你的Mysql密码
        <property>
                <name>javax.jdo.option.ConnectionPassword</name>
                <value>admin</value>
        </property>
		
        <property>
                <name>hive.metastore.schema.verification</name>
                <value>false</value>
        </property>
        
        <property> 
             <name>hive.cli.print.current.db</name>
             <value>true</value>
        </property>
        
        <property> 
                 <name>hive.cli.print.header</name>
                 <value>true</value>
        </property>
        
		<!-- hiveserver2 -->
        <property>
                 <name>hive.server2.thrift.port</name>
                 <value>10000</value>
        </property>

    	<property>
       		<name>hive.server2.thrift.bind.host</name>
       		<value>Master</value>
     	</property>

</configuration>
```

通过下列连接下载MySQL连接包并放至HIVE的lib目录：

```
cd $HIVE_HOME/lib
wget https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.17/mysql-connector-java-8.0.17.jar
```

在mysql端执行如下命令创建HIVE的元数据存储库：

```mysql
create database hivedb;
```

执行HIVE的初始化工作：

```shell
schematool -initSchema -dbType mysql
```

初始化完成后，在Mysql端使用以下指令查看是否初始化成功：

```mysql
use hivedb
show tables
```

若展示出多个数据表，即代表初始化成功。

下面我们使用`beeline`来使用HIVE，注意若你要使用MR，则可以使用`hive`。但在新版本中推荐使用`beeline`,而`beeline`内置使用了Spark。

首先启动`hiveserver2`并令其处于挂起状态：

```shell
cd ..
nohup hiveserver2>> hiveserver2.log 2>&1 &
```

到此处我们的HIVE就安装得差不多的，下面我们针对其进行实战操作。

### 3.应用

创建两个文件用以实践：

```
cd /usr/local
vim t1.txt

#添加以下内容
1
2
3
4
5
6
7
9

vim t2.txt

#添加以下内容
1	a
2   b
3   c
9   x
```

把t2.txt传到hadoop目录下：

```
hdfs dfs -put -f /usr/local/t2.txt /
hdfs dfs -ls /
```

启动`beeline`并使用`!connect jdbc:hive2://127.0.0.1:10000连接hive`：

```
beeline

beeline> !connect jdbc:hive2://127.0.0.1:10000

#弹出的账号输入root，密码可不输入

0: jdbc:hive2://127.0.0.1:10000> show databases;

0: jdbc:hive2://127.0.0.1:10000> select * from t1

0: jdbc:hive2://127.0.0.1:10000> select * from t2;
```

我们还可以使用Spark（或者在hive中使用MR ）进行复杂操作：

```
0: jdbc:hive2://127.0.0.1:10000> select t2.name from t1 left join t2 on t1.id = t2.id;
```

