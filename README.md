# DjangoBlog
本站基于Django2.2及Python3.6开发

## 1. 主要功能
- 文章的撰写与发布
- 评论功能
- 访客留言
- 文章归档及在分类标签下查看

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
### 2.5 测试
```bash
python manage.py runserver
```

## 3.更新日志
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