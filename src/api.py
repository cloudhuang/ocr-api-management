from flasgger import Swagger  # Import Flasgger
from flask import Flask
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app, supports_credentials=True)

# Initialize Swagger inside app context
swagger = Swagger(app)

# Import routes
from src.router import infer_route, claims_route

# Register routes
app.register_blueprint(infer_route.infer_api, url_prefix='/')
app.register_blueprint(claims_route.claims_api, url_prefix='/')

if __name__ == '__main__':
    app.run(port=8000, host='0.0.0.0')


# 启动方法（命令行）
# flask --app src.api run --host 0.0.0.0 --port 8000 --reload
