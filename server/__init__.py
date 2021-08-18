from flask import Flask, render_template

from .api.v1.handlers import api_bp

# Получение главной страницы
def index():
    return render_template(
        "index.html"
    )

server = Flask(__name__)
server.add_url_rule("/", view_func=index)
server.register_blueprint(api_bp, url_prefix="/api/v1")