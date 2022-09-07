import os
from flask import Flask
from dotenv import load_dotenv
from main.routes import main, usuario, poema

def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.register_blueprint(main.app)
    #app.register_blueprint(user.author)
    #app.register_blueprint(poem.poem)
    
    return app