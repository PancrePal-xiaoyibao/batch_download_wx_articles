# 微信文章合集链接提取工具

这是一个用于提取微信公众号文章合集中所有文章链接的工具。

## 功能特点

- 自动提取微信文章合集中的所有文章标题和链接
- 支持自动滚动加载更多内容
- 保存结果为 TXT 和 JSON 格式
- 详细的日志记录系统
- 使用 undetected-chromedriver 避免检测

## 环境要求

- Python 3.9+
- Google Chrome 浏览器
- ChromeDriver（与 Chrome 版本匹配）

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/samqin123/weichat_collection_url_extract.git
cd weichat_collection_url_extract
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 下载 ChromeDriver：
   - 访问 [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/)
   - 下载与您的 Chrome 版本匹配的 ChromeDriver
   - 根据您的操作系统选择对应的安装位置：

     Windows:
     ```bash
     # 创建目录（如果不存在）
     mkdir C:\chromedriver
     # 将下载的 chromedriver.exe 解压到该目录
     # 添加到系统环境变量 PATH 中，或在代码中指定路径：
     driver_path = "C:\\chromedriver\\chromedriver.exe"
     ```

     Linux:
     ```bash
     # 下载并解压 ChromeDriver
     wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.109/linux64/chromedriver-linux64.zip
     unzip chromedriver-linux64.zip

     wget https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.90/mac-arm64/chrome-mac-arm64.zip
     unzip chrome-mac-arm64.zip
     
     # 移动到系统目录并设置权限
     sudo mv chromedriver-linux64/chromedriver /usr/local/bin/
     sudo chmod +x /usr/local/bin/chromedriver
     
     # 在代码中使用
     driver_path = "/usr/local/bin/chromedriver"
     ```

     macOS:
     ```bash
     # 下载并解压 ChromeDriver
     wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.109/mac-x64/chromedriver-mac-x64.zip

     wget https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.90/mac-x64/chromedriver-mac-x64.zip

     unzip chromedriver-mac-x64.zip
     
     # 移动到用户目录
     mkdir -p ~/chromedriver
     mv chromedriver-mac-x64/chromedriver ~/chromedriver/
     
     # 在代码中使用
     driver_path = os.path.expanduser("~/chromedriver/chromedriver")
     ```

   注意：
   - 确保下载的 ChromeDriver 版本与您的 Chrome 浏览器版本匹配
   - Windows 用户可能需要以管理员身份运行命令提示符
   - Linux 用户可能需要使用 sudo 权限
   - 建议将 ChromeDriver 放在系统环境变量中，方便管理和更新

## 使用方法

1. 修改 `extract_links.py` 中的 URL 为您要提取的微信文章合集链接

2. 运行脚本：
```bash
python extract_links.py
```

3. 查看结果：
   - 文章列表将保存在 `articles` 目录下
   - `article_list.txt`: 文本格式
   - `article_list.json`: JSON 格式
   - 运行日志保存在 `logs` 目录下

## 注意事项

- 确保 ChromeDriver 版本与 Chrome 浏览器版本匹配
- 需要稳定的网络连接
- 部分链接可能需要登录微信才能访问

## 问题排查

如果遇到问题：
1. 检查 Chrome 和 ChromeDriver 版本是否匹配
2. 查看 `logs` 目录下的日志文件
3. 确保网络连接正常
4. 检查 URL 是否有效

# 输入链接
https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg4NzUyNDY3NQ==&action=getalbum 
这个格式就可以用了，太长的链接输不进去

