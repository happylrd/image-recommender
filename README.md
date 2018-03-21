# Image Recommender

## Metis

> a crawler and data loader

必要依赖如下：
```
pip install flickrapi
pip install peewee
pip install PyMySQL
```

- [flickrapi](https://stuvel.eu/flickrapi)
- [peewee](http://docs.peewee-orm.com/en/latest/)
- [PyMySQL](https://github.com/PyMySQL/PyMySQL)


### 数据预处理

#### 数据爬取

爬取策略
1. 取100张热门图片，拿到100个（may be less）不同的owner_id。
2. 对每个owner_id，取其所上传的100张图片id（若<100张，则跳过此用户）。
3. 对每个图片id，拿到具体的图片信息，进行一些处理（删掉无用字段）。
4. 为每个用户生成一个json文件（文件名格式为`photo_{owner_id}`），包含该用户上传的100张图片信息。


#### 数据模型生成

借助 [pwiz](http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#pwiz)，一行代码生成数据模型(database -> model.py)：
```
python -m pwiz -e mysql -H localhost -p 3306 -u root -P 123456 image_recommender > model.py
```
每次生成后，只需将 **id字段** 由`BigIntegerField`改为 `BigAutoField`即可。


#### 数据入库

具体逻辑参见[dao.py](https://github.com/happylrd/image-recommender/blob/master/metis/db/dao.py)


#### 数据导出

借助如下sql语句和 [DataGrip](https://www.jetbrains.com/datagrip/?fromMenu)将特定数据从数据库导出为csv文件（共62248条记录），用于之后训练模型。

```sql
SELECT
  u.id,
  p.id,
  t.id
FROM user u, photo p, tag t, photo_tag pt
WHERE u.id = p.owner_id AND p.id = pt.photo_id AND t.id = pt.tag_id
ORDER BY u.id, p.id, t.id
```

数据规模：
用户数 | 图片数 | 标签数 | 图片标签数
--- | --- | --- | ---
93 | 9300 | 12781 | 62248


## Iris

> a api server


### 数据库设计

#### 表结构

##### user表

字段名称 | 类型 | 描述
--- | --- | ---
id | BIGINT AUTO_INCREMENT PRIMARY KEY | 用户id
username | VARCHAR(255) NOT NULL UNIQUE (username) | 用户名
password | VARCHAR(255) NULL | 密码，爬取数据默认123456，真实数据则由用户决定
nickname | VARCHAR(255) NULL | 昵称，爬取数据取realname（可为空）
avatar | VARCHAR(255) NULL | 头像url
create_time | DATETIME NULL | 创建时间

##### photo表

字段名称 | 类型 | 描述
--- | --- | ---
id | BIGINT AUTO_INCREMENT PRIMARY KEY | 图片id
title | VARCHAR(255) NULL | 图片标题
url | VARCHAR(255) NULL | 图片url
owner_id | BIGINT NOT NULL FOREIGN KEY (owner_id) REFERENCES user (id) | 上传者id
create_time | DATETIME NULL | 上传时间

##### tag表

字段名称 | 类型 | 描述
--- | --- | ---
id | BIGINT AUTO_INCREMENT PRIMARY KEY | 标签id
content | VARCHAR(255) NULL | 标签内容（全小写，去空格），用于url及研究
raw | VARCHAR(255) NULL | 标签原始内容（源自用户，未做修改）
create_time | DATETIME NULL | 创建时间

##### photo_tag表

字段名称 | 类型 | 描述
--- | --- | ---
id | BIGINT AUTO_INCREMENT PRIMARY KEY | 无意义自增id
photo_id | BIGINT NOT NULL FOREIGN KEY (photo_id) REFERENCES photo (id) | 图片id
tag_id | BIGINT NOT NULL FOREIGN KEY (tag_id) REFERENCES tag (id) | 标签id
create_time | DATETIME NULL | 创建时间

> 注：photo.title, tag.content, tag.raw字段去掉了所爬取的json数据的emoji。
