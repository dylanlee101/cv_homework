1. 官网下载JDK文件jdk-8u121-linux-x64.tar.gz

```
wget --no-cookies --no-check-certificate --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" "http://download.oracle.com/otn-pub/java/jdk/8u141-b15/336fa29ff2bb4ef291e347e091f7f4a7/jdk-8u141-linux-x64.tar.gz"
```

1. 在opt文件夹下创建一个目录作为JDK的安装目录，比如/opt/java

2. 移动文件到/opt/java目录下

   ```shell
   sudo mv jdk-8u141-linux-x64.tar.gz /opt/java
   ```

3. 解压文件

   ```shell
   cd /opt/java
   tar -zxvf jdk-8u141-linux-x64.tar.gz
   ```

4. 配置环境变量

   ```shell
   vim ~./bashrc
   ```

   末尾加入：

   ```ini
   PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:$JAVA_HOME/bin"
   export CLASSPATH=.:$JAVA_HOME/lib:$JAVA_HOME/jre/lib
   export JAVA_HOME=/opt/java/jdk1.8.0_141
   ```

5. 保存并使环境变量生效

   ```shell
   source ~./bashrc
   ```

6. 判断是否配置成功

   ```shell
   java -version
   ```

