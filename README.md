# QQessence
Python爬虫获取QQ群精华消息

修改借鉴自：User-Time/requests_qq_essence

支持所有格式的精华消息（2023.4.25）
ps:对转发群文件、外部链接（如qq音乐分享）等精华消息，仅支持获取标题、缩略图、文件名（群文件）

可选下载精华消息中的图片，默认3线程（群被封后图片链接都会失效）

请调试运行，在main.py同级目录创建img文件夹并清空

****
2023.10.18

由Maze-is-moon补充，p_skey及skey参数也可登录qq群官网：https://qun.qq.com 从cookie中获取

参考：https://www.52pojie.cn/thread-835096-1-1.html

****

谨以此项目悼念我被tx封掉的积累上百条精华消息的旧群(2022.11.4)![image](https://user-images.githubusercontent.com/105963780/234330957-7916ff46-f98a-42b0-bcb1-21d3c0b8eac6.png)
