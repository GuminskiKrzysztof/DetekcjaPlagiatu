from flask import Flask
from controller.project_controller import project_bp
from controller.api_controller import api_bp

app = Flask(__name__,
            template_folder='view/templates',
            static_folder='view/static',
            static_url_path='/static')

# Register blueprints with URL prefixes
app.register_blueprint(project_bp, url_prefix='/')
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
