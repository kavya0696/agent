from flask import Flask, render_template
from app.youtube import youtube_bp


def create_app():

    app = Flask(__name__)

    app.register_blueprint(
        youtube_bp,
        url_prefix="/youtube"
    )

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/html")
    def html():
        return render_template("index.html")

    return app 
