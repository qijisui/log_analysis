运行环境：Linux
适用版本：android P
脚本作用：提取logcat log中蓝牙相关log，便于debug。
脚本用法： 
//将脚本放置到/usr/bin/之后可以在任意终端中执行
#btAnalysis  //连接手机实时抓取logcat解析
#btAnalysis  xxx    //解析已抓取的名为“xxx”的log文件，本地同时会生成xxx.bt的文件