# log_analysis说明文档
## 脚本介绍：
提取logcat log中蓝牙相关log，便于debug。

## 运行环境：Linux
## 适用版本：Android P
## Python版本：Python 2.x

## 脚本运行： 
将脚本放置到/usr/bin/之后可以在任意终端中执行
```
#btAnalysis        //连接手机实时抓取logcat解析
#btAnalysis xxx    //解析“xxx”路径下的单个或者全部log文件，本地同时会生成xxx.bt的文件
```
