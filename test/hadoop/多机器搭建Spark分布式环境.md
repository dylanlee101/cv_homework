### 1.初始准备：

- 准备3台虚拟机，其IP分别为：

```
192.168.42.128
192.168.42.129
192.168.42.130
```

- 需要安装好JDK，环境生效即可
- 安装好Hadoop集群

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

- Master作为Master、Worker
- Slave1作为Worker
- Slave2也是作为Worker

### 3.安装SBT

sbt是一个simple build tools，可以进行scala与java的项目管理，支持增量编译，内置scala console。可以简单将SBT看做是Scala世界的Maven，虽然二者各有优劣，但完成的工作基本是类似的。

- 确保已经安装JDK1.8并正确配置环境

在<https://www.scala-sbt.org/1.x/docs/Installing-sbt-on-Linux.html>进行SBT的下载里面有更方便的利用资源管理器进行下载的方式。此处我们选择使用压缩包进行下载：

```shell
cd /usr/local
wget https://piccolo.link/sbt-1.2.8.zip
unzip sbt-1.2.8.zip
rm sbt-1.2.8.zip
```

进行环境配置：

```vim
vim ~/.bash_profile
# 添加如下内容
export SBT_HOME="/usr/local/sbt"
export PATH=$PATH:$SBT_HOME/bin

source ~/.bash_profile
```

下面进行测试，从GitHub拉下一个`hello-world`的模板，：

```shell
mkdir test
cd test
sbt new scala/hello-world.g8
```

当出现提示时，将应用程序命名为`hello-world`，此时便创建好了一个项目。让我们运行一下：

```shell
cd hello-world
sbt
~run
```

使用run我们可以运行当前工程文件，而`~`是一个可选项，代表当工程中的任意文件被保存时，重新运行项目。从而允许快速编辑/运行/调试。

如果你只想搭建一个Spark，在此处便可以直接调到下一个大项：第四点。

我们可以打开另外一个终端来尝试修改scala文件，以查看`~`的作用（选做）：

```shell
vim src/main/scala/Main.scala # 将Hello,World 改成 Hello 
```

当你保存该文件时，若sbt command仍然没有关闭，你便可以看到该终端输出了`Hello`。

我们还可以使用如下方式使用已发布的库为应用程序添加额外的功能。

```shell
vim build.sbt
# 添加以下内容
libraryDependencies += "org.scala-lang.modules" %% "scala-parser-combinators" % "1.1.0"
```

build.sbt相当于Maven的pom.xml。通过使用+=，我们将scala-parser-combinator依赖项添加到依赖项集中，sbt将在启动时去获取这些依赖项。我们可以在Scala库索引[Scaladex](https://index.scala-lang.org/)上找到更多已发布的库。

在使用SBT运行程序的过程中，我们也可以使用测试程序来测试我们代码的正确性与可用性。在本教程中，我们将演示一个来自ScalaTest框架的流行选项，称为FunSuite。

```shell
cd /usr/local/test
sbt new scala/scalatest-example.g8
ScalaTestTutorial # 命名
cd ScalaTestTutorial
sbt test
```

使用`sbt test`命令将可以使用一个名为CubeCalculator.cube的测试运行测试套件CubeCalculatorTest来测试我们的程序。

我们可以发现该项目有如下两个文件：

- `src/main/scala/CubeCalculator.scala`
- `src/test/scala/CubeCalculatorTest.scala`

在`CubeCalculator.scala`中定义了方法`cube`。在`CubeCalculatorTest.scala`中我们可以看到如下的测试方法：

```java
import org.scalatest.FunSuite

class CubeCalculatorTest extends FunSuite {
	test("CubeCalculator.cube") {
		assert(CubeCalculator.cube(3) === 27)
	}
}
```

`extends FunSuite`让我们使用ScalaTest的FunSuite类的功能来使用测试函数。`CubeCalculator.cube(3)`调用了方法。

### 4.安装scala

 Scala 是一门多范式（multi-paradigm）的编程语言，设计初衷是要集成面向对象编程和函数式编程的各种特性。Scala 运行在Java虚拟机上，并兼容现有的Java程序。Scala 源代码被编译成Java字节码，所以它可以运行于JVM之上，并可以调用现有的Java类库。

在<https://www.scala-lang.org/download/>底部可以进行相应版本压缩包的下载

```shell
cd /usr/local
wget https://downloads.lightbend.com/scala/2.13.0/scala-2.13.0.tgz
tar -zxvf scala-2.13.0.tgz
rm scala-2.13.0.tgz
```

修改环境变量

```shell
vim ~/.bash_profile
# 添加以下内容
export SCALA_HOME="/usr/local/scala-2.13.0"
export PATH=$PATH:$SCALA_HOME/bin
```

测试：

```shell
scala
Welcome to Scala version 2.11.7 (Java HotSpot(TM) 64-Bit Server VM, Java 1.8.0_101).
Type in expressions to have them evaluated.

scala>
```

### 5.安装Spark

Spark官网：<http://spark.apache.org/>

```shell
cd /usr/local
wget http://mirror.bit.edu.cn/apache/spark/spark-2.4.3/spark-2.4.3-bin-hadoop2.7.tgz
tar -zxvf spark-2.4.3-bin-hadoop2.7.tgz
rm spark-2.4.3-bin-hadoop2.7.tgz
```

设置环境变量：

```shell
vim ~/.bash_profile
# 添加以下内容
export SPARK_HOME="/usr/local/spark-2.4.3-bin-hadoop2.7"
export PATH=PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

source ~/.bash_profile
```

设置配置文件：

```shell
cd spark-2.4.3-bin-hadoop2.7
cp spark-env.sh.template spark-env.sh
vim spark-env.sh
# 添加以下内容
export JAVA_HOME="/opt/java/jdk1.8.0_141"
export HADOOP_CONF_DIR="/usr/local/hadoop-2.7.7/etc/hadoop"
export SCALA_HOME="/usr/local/scala-2.13.0"
export SPARK_MASTER_IP=Master
export SPARK_WORKER_CORES=2
export SPARK_WORKER_MEMORY=2g

cp slaves.template slaves
# 修改为以下内容
Master
Slave1
Slave2
```

在Master主机中将上述使用的文件复制到其余两台机器中：

```shell
rsync -av /usr/local/spark-2.4.3-bin-hadoop2.7 Slave1:/usr/local/spark-2.4.3-bin-hadoop2.7
rsync -av /usr/local/sbt Slave1:/usr/local/sbt
rsync -av /usr/local/scala-2.13.0 Slave1:/usr/local/scala-2.13.0

rsync -av /usr/local/spark-2.4.3-bin-hadoop2.7 Slave2:/usr/local/spark-2.4.3-bin-hadoop2.7
rsync -av /usr/local/sbt Slave2:/usr/local/sbt
rsync -av /usr/local/scala-2.13.0 Slave2：/usr/local/scala-2.13.0
```

在Master主机中启动Spark，注意`start-all.sh`，在Hadoop中有同名执行文件，因此此处我们不使用环境变量执行执行文件：

```shell
sbin/start-all.sh
```

Master主机 jps 查看到多出一个Master，worker进程，其他两台主机查看到多出一个worker进程