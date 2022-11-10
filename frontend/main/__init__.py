import os
from flask import Flask
from dotenv import load_dotenv
from main.routes import main, poema, usuario

def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.register_blueprint(main.app)


    app.config['API_URL'] = os.getenv('API_URL')
    

    
    return app