# DB_learn

![](<https://github.com/KXXH/DB_learn/workflows/test/badge.svg>)
[![codecov](https://codecov.io/gh/KXXH/DB_learn/branch/master/graph/badge.svg)](https://codecov.io/gh/KXXH/DB_learn)
 
 a simple work for db_design

## 环境配置方法

1. 先在*项目根目录*下输入指令`python -m venv venv`
2. 再在根目录下输入`venv\Scripts\activate`
3. 然后在venv下使用指令`pip install -r requirements.txt`

## 数据库配置

**要使用数据库，需要在`free_shark`目录下创建一个`db_config.cfg`配置文件，注明下列参数**：

| 字段 | 含义 |
| ------- | ----- |
| DB_PORT | 数据库端口 |
| DB_HOST | 数据库域名 |
| DB_USER | 数据库用户名 |
| DB_PASSWORD | 数据库密码 |
| DB_CHARSET | 数据库编码 |
| DB_DATABASE | 数据库名称 |



