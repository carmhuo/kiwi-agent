import logging
from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

        # 配置日志
    app.logger.setLevel(logging.INFO)
    handler = logging.FileHandler('app.log')
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    app.logger.addHandler(handler)

    # Import and register blueprints here
    from react_app import routes
    app.register_blueprint(routes.bp)

    return app