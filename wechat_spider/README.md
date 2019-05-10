# 搜狗微信基于关键词爬取相关微信公众号文章

* 基于Scrapy 框架

* 利用selenium + phantomjs 进行页面渲染

* 存取爬取的内容到MongoDB

* 利用BeautifulSoup进行爬取免费代理网站IP，设计IP代理池和请求池

## 爬取IP并存入数据库

运行`wechatpub`目录下的`getproxy.py`文件，爬取IP，存入MongoDB；

## 根据关键词爬取文章链接

在项目目录下，键入命令：

```python
# scrapy crawl pubinfospider
```

提示输入搜索关键词后键入关键词，即开始爬取，爬取的文章链接存入数据库；

## 根据存取的文章链接爬取文章

在项目目录下，键入命令：

```python
# scrapy crawl postspider
```

爬取并存入数据库。
