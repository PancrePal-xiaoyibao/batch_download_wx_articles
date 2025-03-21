开发目的：
参考 和 创建一个新python文件，实现对指定公众号合集的模拟滑动，获取完整的url，标题，输出txt和json，并进一步利用api提取文章，输出到指定目录。

开发要求：
1.创建新文件，不要修改原来文件。

2.采用交互式执行，第一步让用户输入公众号合集url，需要支持长链接，比如https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MjM5MzAwMjcyMA==&action=getalbum&album_id=1583051650129313793&scene=173&sessionid=undefined&enterid=0&from_msgid=2653473624&from_itemidx=3&count=3&nolastread=1&uin=&key=&devicetype=iMac+MacBookPro18%2C1+OSX+OSX+14.5+build(23F79)&version=13080a10&lang=zh_CN&nettype=WIFI&ascene=0&fontScale=100

3.输入校验通过后，第二步提醒用户输入保存获取url的json,txt文件地址，下载文件自动创建在同一个目录地址下的download_content中。

4.逻辑使用/Users/qinxiaoqiang/Downloads/公众号下载jina2md/coding/批量提取公众号url结合网页工具下载/crawn_link.py和/Users/qinxiaoqiang/Downloads/公众号下载jina2md/coding/批量提取公众号url结合网页工具下载/batch_webreader_to_markdown.py，这两个文件都是可以正常运行。