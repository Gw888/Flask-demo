# Flask Demo 用户管理系统

## 项目简介
本项目是一个用 Flask（轻量级Web框架）开发的用户管理系统，支持用户的增删改查（CRUD）。

## 主要技术/名词解释
- Flask：Python的Web开发框架，类似Java的Spring Boot。
- ORM（Object Relational Mapping）：对象关系映射，。
- SQLAlchemy（SQL ài kè mì）：ORM库。
- Marshmallow（mǎ shì mǎ lòu）：序列化/反序列化库，把对象和JSON互转。
- Migrate（mái géi tè）：数据库迁移工具，管理表结构变更。
- Blueprint（蓝图）：Flask的路由分组机制，类似Java的Controller分包。
- API：前后端通信的标准方式。

## 运行步骤
1. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```
2. 配置数据库（.env文件）
3. 初始化数据库
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```
4. 启动项目
   ```bash
   python run.py
   ```
5. 访问 http://127.0.0.1:5000

## 常用API
- GET `/api/users` 获取用户列表（支持分页、搜索）
- POST `/api/users` 新增用户
- PUT `/api/users/<id>` 修改用户
- DELETE `/api/users/<id>` 删除用户

## 响应格式
```json
{
  "code": 200,
  "message": "操作成功",
  "data": {}
}
```
```

---

如需我自动为所有相关文件加注释，请告诉我你想优先注释哪些文件（比如 models、schemas、api、upload、run.py 等），我可以自动帮你加上！  
如需拼音标注更详细，也可以告诉我！