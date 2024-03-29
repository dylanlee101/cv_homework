### 1.初始准备：

- 准备3台虚拟机，其IP分别为：

```
192.168.42.128
192.168.42.129
192.168.42.130
```

- 需要安装好JDK，环境生效即可
- 根据之前的教程安装好Zookeeper

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

### 3.Kafka安装

此处我们选择下载的是`kafka 2.12-2.3.0`版本，下载路径如下：http://mirror.bit.edu.cn/apache/kafka/2.3.0/kafka_2.12-2.3.0.tgz。各位也可以在此处<http://mirror.bit.edu.cn/apache/kafka/>挑选其他版本。

```shell
cd /usr/local
wget http://mirror.bit.edu.cn/apache/kafka/2.3.0/kafka_2.12-2.3.0.tgz
tar -zxvf kafka_2.12-2.3.0.tgz
rm kafka_2.12-2.3.0.tgz
```

安装完成之后我们需要对其进行配置，主要需要关注的为`server.properties`这个文件。

该文件中各个参数的解释如下：

```shell
broker.id=0  #当前机器在集群中的唯一标识，和zookeeper的myid性质一样
port=19092 #当前kafka对外提供服务的端口默认是9092
host.name=192.168.7.100 #这个参数默认是关闭的，在0.8.1有个bug，DNS解析问题，失败率的问题。
num.network.threads=3 #这个是borker进行网络处理的线程数
num.io.threads=8 #这个是borker进行I/O处理的线程数
log.dirs=/opt/kafka/kafkalogs/ #消息存放的目录，这个目录可以配置为“，”逗号分割的表达式，上面的num.io.threads要大于这个目录的个数这个目录，如果配置多个目录，新创建的topic他把消息持久化的地方是，当前以逗号分割的目录中，那个分区数最少就放那一个
socket.send.buffer.bytes=102400 #发送缓冲区buffer大小，数据不是一下子就发送的，先回存储到缓冲区了到达一定的大小后在发送，能提高性能
socket.receive.buffer.bytes=102400 #kafka接收缓冲区大小，当数据到达一定大小后在序列化到磁盘
socket.request.max.bytes=104857600 #这个参数是向kafka请求消息或者向kafka发送消息的请请求的最大数，这个值不能超过java的堆栈大小
num.partitions=1 #默认的分区数，一个topic默认1个分区数
log.retention.hours=168 #默认消息的最大持久化时间，168小时，7天
message.max.byte=5242880  #消息保存的最大值5M
default.replication.factor=2  #kafka保存消息的副本数，如果一个副本失效了，另一个还可以继续提供服务
replica.fetch.max.bytes=5242880  #取消息的最大直接数
log.segment.bytes=1073741824 #这个参数是：因为kafka的消息是以追加的形式落地到文件，当超过这个值的时候，kafka会新起一个文件
log.retention.check.interval.ms=300000 #每隔300000毫秒去检查上面配置的log失效时间（log.retention.hours=168 ），到目录查看是否有过期的消息如果有，删除
log.cleaner.enable=false #是否启用log压缩，一般不用启用，启用的话可以提高性能
zookeeper.connect=192.168.7.100:12181,192.168.7.101:12181,192.168.7.107:1218 #设置zookeeper的连接端口
```

此处我们需要修改以下内容：

```shell
broker.id=1
zookeeper.connect=Master:2181,Slave1:2181,Slave2:2181
```

设置环境变量：

```shell
vim ~/.bash_profile
export KAFKA_HOME="/usr/local/kafka_2.12-2.3.0"
export PATH=$PATH:$KAFKA_HOME/bin

source ~/.bash_profile
```

接着我们需要把`Kafka`与配置文件移植到其他两台机器：

```shell
rsync -av /usr/local/kafka_2.12-2.3.0 Slave1:/usr/local/kafka_2.12-2.3.0
rsync -av /usr/local/kafka_2.12-2.3.0 Slave2:/usr/local/kafka_2.12-2.3.0

rsync -av ~/.bash_profile Slave1:~/.bash_profile
rsync -av ~/.bash_profile Slave2:~/.bash_profile
```

在其他两台机器中我们还需要进行如下操作：

```shell
source ~/.bash_profile
vim $KAFKA_HOME/config/server.properties

# 将其中的broker.id分别修改，Slave1改为2,Slave2改为3，集群内部配置不相同即可。
```

最后依次在各个机器上启动Kafka：

```
cd $KAFKA_HOME/config
kafka-server-start.sh -daemon server.properties
```

### 4.检查安装

创建topic：

```shell
kafka-topics.sh --create --zookeeper Master:2181 --replication-factor 2 --partitions 1 --topic test
```

查看topic：

```shell
kafka-topics.sh --list --zookeeper Master:2181
```

查看topic状态：

```shell
kafka-topics.sh --describe --zookeeper Master:2181 --topic test
```

在一台服务器上创建一个发布者：

```shell
kafka-console-producer.sh --broker-list Master:9092 --topic test
```

在另外一台服务器上创建一个消费者：

```shell
kafka-console-consumer.sh --bootstrap-server Master:9092 --topic test
```

分别建立成功后在发布者中发布的消息可以在消费者中被接收到。