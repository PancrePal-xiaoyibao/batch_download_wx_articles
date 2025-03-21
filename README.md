# 微信公众号文章批量下载工具

这是一个用于自动化批量下载微信公众号文章的工具，支持从公众号合集或文章列表中提取文章并转换为Markdown格式。

## 功能特点

- 支持从微信公众号合集或文章列表中批量提取文章
- 自动提取文章标题和URL
- 自动去重并按时间排序
- 支持将文章转换为Markdown格式
- 保留原文格式，包括图片、表格等

## 环境配置

### 1. Python环境

确保您的系统已安装Python 3.7或更高版本。

### 2. 安装ChromeDriver

本工具使用ChromeDriver进行网页内容提取，请按以下步骤安装：

1. 查看Chrome浏览器版本：
   - 打开Chrome浏览器
   - 点击右上角三个点 > 帮助 > 关于Google Chrome
   - 记录版本号（如：131.0.6778.204）

2. 下载对应版本的ChromeDriver：
   - 访问 [ChromeDriver下载页面](https://googlechromelabs.github.io/chrome-for-testing/)
   - 选择与Chrome浏览器相同主版本号的ChromeDriver
   - 下载对应操作系统的版本

3. 配置ChromeDriver：

   **验证ChromeDriver适配性：**
```bash
# 检查ChromeDriver版本
chromedriver --version

# 检查Chrome浏览器版本
# macOS:
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version
# Windows:
reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version

# 验证ChromeDriver是否正常工作
python -c "from selenium import webdriver; driver = webdriver.Chrome(); print('ChromeDriver工作正常！'); driver.quit()"
```

   如果出现版本不匹配问题，请确保：
   - Chrome浏览器和ChromeDriver的主版本号相同
   - ChromeDriver已正确添加到系统PATH
   - 使用了正确的操作系统版本（x64/arm64）
   - 重新下载匹配版本的ChromeDriver

   **macOS：**
```bash
# 下载ChromeDriver（以134.0.6998.90版本为例）
# 对于Intel芯片(x64)：
wget https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.90/mac-x64/chromedriver-mac-x64.zip
# 对于Apple芯片(arm64)：
wget https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.90/mac-arm64/chromedriver-mac-arm64.zip

# 解压文件（根据下载的版本选择对应文件名）
unzip chromedriver-mac-x64.zip  # 或 chromedriver-mac-arm64.zip

# 创建并移动到用户目录（推荐）
mkdir -p ~/chromedriver
mv chromedriver-mac-x64/chromedriver ~/chromedriver/  # 或 chromedriver-mac-arm64/chromedriver

# 添加执行权限
chmod +x ~/chromedriver/chromedriver

# 添加到环境变量（可选）
echo 'export PATH="$HOME/chromedriver:$PATH"' >> ~/.zshrc  # 如果使用zsh
# 或
echo 'export PATH="$HOME/chromedriver:$PATH"' >> ~/.bash_profile  # 如果使用bash
source ~/.zshrc  # 或 source ~/.bash_profile
```

   **Windows：**
   - 解压下载的zip文件
   - 将chromedriver.exe移动到Python安装目录或系统PATH中的任意目录
   - 或添加chromedriver.exe所在目录到系统环境变量Path中

   **代码配置：**
   在Python代码中使用以下方式指定ChromeDriver路径：
```python
import os

# 获取用户目录下的ChromeDriver路径
driver_path = os.path.expanduser("~/chromedriver/chromedriver")
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. API密钥配置

1. 创建并配置.env文件：
```bash
# 创建.env文件
touch .env

# 编辑文件，添加API密钥
echo "WEB_READER_API_KEY=your_api_key_here" > .env
```

2. 获取API密钥：
   - 联系Vlinic购买获取apikey
   - 将获取的密钥替换.env文件中的your_api_key_here

## 使用方法

### 1. 运行脚本

```bash
python wechat_to_markdown.py
```

### 2. 输入参数

1. 输入公众号合集链接或文章链接，支持以下格式：
   - 合集链接：https://mp.weixin.qq.com/mp/appmsgalbum?__biz=xxx&action=getalbum&album_id=xxx
   - 文章链接：https://mp.weixin.qq.com/s/xxx

2. 指定输出目录（默认为converted_files）

### 3. 等待下载

程序会自动：
1. 提取文章链接
2. 下载文章内容
3. 转换为Markdown格式
4. 保存到指定目录

## 常见问题

1. **Q: ChromeDriver版本不匹配怎么办？**
   A: 确保下载的ChromeDriver版本与Chrome浏览器的主版本号相同。例如，Chrome版本为131.0.6778.204，则需要下载131.x.xxxx.xx版本的ChromeDriver。

2. **Q: 提示找不到ChromeDriver怎么办？**
   A: 检查ChromeDriver是否正确安装并添加到系统PATH。可以在终端运行`chromedriver --version`验证安装。

3. **Q: 下载失败怎么办？**
   A: 
   - 检查网络连接是否稳定
   - 确认API密钥是否正确配置
   - 验证输入的链接格式是否正确
   - 检查ChromeDriver是否正常运行

4. **Q: 如何获取API密钥？**
   A: 请联系Vlinic购买获取apikey，获取后配置到.env文件中。

## 注意事项

1. 确保系统已安装Chrome浏览器
2. 保持网络连接稳定
3. API密钥请妥善保管，不要泄露
4. 如果文章数量较多，建议分批次处理

## 许可证

MIT License