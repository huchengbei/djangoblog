# DjangoBlog
本站基于Django2.2及Python3.6开发

## 1. 主要功能
- 文章的撰写与发布(支持Markdown)
- 评论、留言功能
- 文章归档及在分类标签下查看
- 实现用户的注册、登录、注销, 支持第三方登录
- 自定义导航栏
- 可配置分析代码，页面底部自动显示信息

## 2. 本地安装
### 2.1 下载仓库
```bash
git clone https://github.com/huchengbei/DjangoBlog.git
```
### 2.2 安装环境
```bash
pip install -r requirements.txt
```
### 2.3 修改配置文件并迁移数据库
修改 djangoblog/settins.py中的数据库信息
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2.4 创建超级用户
```bash
python manage.py createsuperuser
```
### 2.5 测试
```bash
python manage.py runserver
```

### 2.6 设置网站信息
运行之后必须先进后台`/admin`在`Blog`进行`网站配置`

否则无法使用

## 3.更新日志
### V2.0

- 改版界面UI，使用BootStrap4构建
- 实现用户的注册、登录、注销
- 第三方登录，支持Github登录
- 更改评论界面，具有多级样式
- 缩短摘要长度，使界面更简洁
- 后端编辑Markdown文章实时预览
- 评论可以审核，并添加了anti_spam字段，有值则为垃圾
- 修复部分bug



### V1.0
2019年9月9日，正式将博客改版上线

- 文章的撰写与发布
- 评论功能
- 访客留言
- 文章归档及在分类标签下查看
- 自定义账户类
- 定制站点信息
- 可定制侧边栏
- 支持MarkDown
