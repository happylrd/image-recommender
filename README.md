# Image Recommender

## Metis

> A crawler, data loader, and image recommender.

必要依赖如下：
```
pip install flickrapi
pip install peewee  # conda install -c conda-forge peewee
pip install PyMySQL
```

- [flickrapi](https://stuvel.eu/flickrapi)
- [peewee](https://anaconda.org/conda-forge/peewee)
- [PyMySQL](https://github.com/PyMySQL/PyMySQL)


### 数据处理

#### 数据爬取

爬取策略（older）
1. 取100张热门图片，拿到100个（may be less）不同的owner_id。
2. 对每个owner_id，取其所上传的100张图片id（若<100张，则跳过此用户）。
3. 对每个图片id，拿到具体的图片信息，进行一些处理（删掉无用字段）。
4. 为每个用户生成一个json文件（文件名格式为`photo_{owner_id}`），包含该用户上传的100张图片信息。


#### 数据模型生成

借助 [pwiz](http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#pwiz)，一行代码生成数据模型(database -> model.py)：
```
python -m pwiz -e mysql -H localhost -p 3306 -u root -P 123456 image_recommender > model.py
```
每次生成后，只需将 **id字段** 由`BigIntegerField`改为 `BigAutoField`，`charset`的值 改为 `utf8mb4`即可。


#### 数据入库

##### 修改MySQL的字符集为utf8mb4

1. 修改配置文件 `my.ini`
```
# 对本地的mysql客户端的配置
[client]
default-character-set = utf8mb4

# 对其他远程连接的mysql客户端的配置
[mysql]
default-character-set = utf8mb4

# 本地mysql服务的配置
[mysqld]
character-set-client-handshake = FALSE
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
init_connect = 'SET NAMES utf8mb4'
```

2. 执行以下步骤
```
net stop mysql57 // 停止mysql服务
net start mysql57 // 启动mysql服务

mysql -u root -p // 回车后输入密码，登录本地mysql

// 查看当前系统默认的字符集设置
SHOW VARIABLES WHERE Variable_name LIKE 'character\_set\_%' OR Variable_name LIKE 'collation%';

// 让 character_set_server 为 utf8mb4，每次重启mysql服务都要重新设置（每次开机都要执行此命令）。
set global character_set_server=utf8mb4;
set session character_set_server=utf8mb4;

// 让 character_set_database 为 utf8mb4，新数据库不需要执行这条命令
ALTER DATABASE image_recommender CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

// 之前的配置
mysql> SHOW VARIABLES WHERE Variable_name LIKE 'character\_set\_%' OR Variable_name LIKE 'collation%';
+--------------------------+-----------------+
| Variable_name            | Value           |
+--------------------------+-----------------+
| character_set_client     | gbk             |
| character_set_connection | gbk             |
| character_set_database   | utf8            |
| character_set_filesystem | binary          |
| character_set_results    | gbk             |
| character_set_server     | utf8            |
| character_set_system     | utf8            |
| collation_connection     | gbk_chinese_ci  |
| collation_database       | utf8_general_ci |
| collation_server         | utf8_general_ci |
+--------------------------+-----------------+
10 rows in set, 1 warning (0.00 sec)

// 现在的配置
mysql> use image_recommender;
Database changed
mysql> SHOW VARIABLES WHERE Variable_name LIKE 'character\_set\_%' OR Variable_name LIKE 'collation%';
+--------------------------+--------------------+
| Variable_name            | Value              |
+--------------------------+--------------------+
| character_set_client     | utf8mb4            |
| character_set_connection | utf8mb4            |
| character_set_database   | utf8mb4            |
| character_set_filesystem | binary             |
| character_set_results    | utf8mb4            |
| character_set_server     | utf8mb4            |
| character_set_system     | utf8               |
| collation_connection     | utf8mb4_general_ci |
| collation_database       | utf8mb4_general_ci |
| collation_server         | utf8mb4_general_ci |
+--------------------------+--------------------+
10 rows in set, 1 warning (0.00 sec)
```

参考
- [修改MySQL的字符集为utf8mb4](https://docs.lvrui.io/2016/08/21/%E4%BF%AE%E6%94%B9MySQL%E7%9A%84%E5%AD%97%E7%AC%A6%E9%9B%86%E4%B8%BAutf8mb4/)
- [mysql/Java服务端对emoji的支持](https://segmentfault.com/a/1190000000616820)

数据入库具体逻辑参见[dao.py](https://github.com/happylrd/image-recommender/blob/master/metis/db/dao.py)

数据规模：

用户数 | 图片数 | 标签数 | 图片标签数 | 喜欢数
--- | --- | --- | --- | ---
23259 | 8837 | 19368 | 117327 | 88370


#### 数据导出

借助如下sql语句和 [DataGrip](https://www.jetbrains.com/datagrip/?fromMenu)将特定数据从数据库导出为csv文件，用于之后训练模型。

```sql
/*
fileName: user_photo_fav.csv
rowNum: 88370
isRedundant: false
 */
SELECT
  f.user_id,
  f.photo_id,
  f.is_fav
FROM favorite f
ORDER BY f.user_id, f.photo_id


/*
fileName: photo_tag.csv
rowNum: 117327
isRedundant: true
 */
SELECT
  pt.photo_id,
  pt.tag_id
FROM photo_tag pt
ORDER BY pt.photo_id, pt.tag_id
```


### 推荐算法

#### TopN

#### Tag-Based

1. 构建图片-标签矩阵
2. 依据图片向量计算相似度（以匹配的标签个数来衡量），推荐最相似的图片

#### ItemCF

1. 构建用户-图片评分矩阵
2. 依据评分矩阵的转置来计算图片之间的相似度，得到图片相似度矩阵（同现矩阵）
3. 根据 `推荐结果 = 评分矩阵 * 同现矩阵`，得到推荐结果，并进行归一化。


## Iris

> A api server for image recommender.

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
f_view_num | INT NULL | flickr View个数，仅用于分析
f_fav_num | INT NULL | flickr Fav个数，仅用于分析
f_comment_num | INT NULL | flickr Comment个数，仅用于分析
create_time | DATETIME NULL | 上传时间

##### tag表

字段名称 | 类型 | 描述
--- | --- | ---
id | BIGINT AUTO_INCREMENT PRIMARY KEY | 标签id
content | VARCHAR(255) NULL | 标签内容（全小写，去空格），用于url及研究
raw | VARCHAR(255) NULL | 标签原始内容（源自用户，未做修改），用于UI展示
create_time | DATETIME NULL | 创建时间


##### photo_tag表

字段名称 | 类型 | 描述
--- | --- | ---
id | BIGINT AUTO_INCREMENT PRIMARY KEY | 无意义自增id
photo_id | BIGINT NOT NULL FOREIGN KEY (photo_id) REFERENCES photo (id) | 图片id
tag_id | BIGINT NOT NULL FOREIGN KEY (tag_id) REFERENCES tag (id) | 标签id
create_time | DATETIME NULL | 创建时间


##### favorite表

字段名称 | 类型 | 描述
--- | --- | ---
id | BIGINT AUTO_INCREMENT PRIMARY KEY | 无意义自增id
user_id | BIGINT NOT NULL FOREIGN KEY (user_id) REFERENCES user (id) | 用户id
photo_id | BIGINT NOT NULL FOREIGN KEY (photo_id) REFERENCES photo (id) | 图片id
is_fav | INT NULL | 是否喜欢，0不喜欢，1喜欢
create_time | DATETIME NULL | 创建时间


##### user_photo_rec表

字段名称 | 类型 | 描述
--- | --- | ---
id | BIGINT AUTO_INCREMENT PRIMARY KEY | 无意义自增id
user_id | BIGINT NOT NULL UNIQUE | 用户id
rec_photo_ids | VARCHAR(255) NULL | 推荐图片id列表（以逗号分隔的字符串存储）
create_time | DATETIME NULL | 创建时间


##### photo_photo_rec表

字段名称 | 类型 | 描述
--- | --- | ---
id | BIGINT AUTO_INCREMENT PRIMARY KEY | 无意义自增id
photo_id | BIGINT NOT NULL UNIQUE | 图片id
rec_photo_ids | VARCHAR(255) NULL | 推荐图片id列表（以逗号分隔的字符串存储）
create_time | DATETIME NULL | 创建时间


> 注：文本字段可能有emoji，且有些 emoji被识别成普通文本，导致`photo_tag.csv`有冗余。


### Dependence

- **spring-boot**
- spring mvc
- spring
- spring-data-jpa
- spring-security
- [jjwt](https://github.com/jwtk/jjwt)
- gradle


## Venus

> A mobile web app for image recommender.


### Dependence

- **vue**
- vue-router
- axios
- [vuetify](https://github.com/vuetifyjs/vuetify)
- vue-cli with PWA support
  - webpack
