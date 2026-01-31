from flask import Flask
import os
import config

def create_app():
    """Create and configure the Flask application"""
    # Get the base directory (parent of app folder)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    template_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'static')

    app = Flask(__name__,
                template_folder=template_dir,
                static_folder=static_dir)

    # Load configuration
    app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
    app.config['OUTPUT_FOLDER'] = config.OUTPUT_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
    app.config['SECRET_KEY'] = config.SECRET_KEY

    # Register blueprints
    from app.routes.detection import detection_bp
    from app.routes.webcam import webcam_bp

    app.register_blueprint(detection_bp)
    app.register_blueprint(webcam_bp)

    return app
