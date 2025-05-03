from flask import Flask, send_from_directory  # Flask是Web框架的核心对象，send_from_directory用于返回静态文件
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy是ORM工具
from flask_marshmallow import Marshmallow  # Marshmallow用于对象和JSON的序列化/反序列化
from flask_migrate import Migrate  # Migrate用于数据库结构迁移
from dotenv import load_dotenv  # 用于加载.env文件中的环境变量
import os  # Python标准库，处理文件路径、环境变量等

# 加载 .env 文件中的环境变量（如数据库连接等敏感信息）
load_dotenv()

# 初始化数据库扩展（SQLAlchemy 用于ORM数据库操作）
db = SQLAlchemy()
# 初始化序列化扩展（Marshmallow 用于对象与JSON互转）
ma = Marshmallow()
# 初始化数据库迁移扩展（Migrate 用于数据库结构变更管理）
migrate = Migrate()

# Flask应用工厂函数，创建并配置Flask实例
# 这样可以方便地进行测试和多环境部署
# static_folder 指定静态文件目录，static_url_path 指定静态文件URL前缀

def create_app():
    app = Flask(
        __name__,
        static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'),
        static_url_path='/static'
    )
    
    # 配置数据库连接（从环境变量读取，推荐用.env文件管理敏感信息）
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    # 关闭SQLAlchemy的修改追踪（节省资源）
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # 返回的JSON不自动按key排序，保持原顺序
    app.config['JSON_SORT_KEYS'] = False
    
    # 初始化所有扩展（将app对象传递给各扩展）
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    
    # 注册API蓝图（将所有API路由挂载到/app/api目录下，前缀为/api）
    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # 兜底路由：所有非API的请求都返回前端页面（支持前端路由刷新）
    # 例如：访问 /、/user/1、/about 都返回 index.html
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        # 如果请求的静态文件存在，则直接返回该文件
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            # 否则返回前端主页面（index.html），支持SPA前端路由
            return send_from_directory(app.static_folder, 'index.html')
    
    return app 