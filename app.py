from flask import Flask, jsonify
from controllers.tweet_controller import tweet_bp
from controllers.sentiment_controller import sentiment_bp
from models.tweet_model import Base
from utils.db import engine
import yaml

def load_config(config_path='config.yaml'):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

config = load_config()

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(tweet_bp, url_prefix='/api')
    app.register_blueprint(sentiment_bp, url_prefix='/api')

    # Initialize Database
    Base.metadata.create_all(bind=engine)

    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to the Sentiment Analysis API"}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
