from config import create_app
from flask_cors import CORS
from utils.extentions import bcrypt, jwt

app = create_app()

bcrypt.init_app(app)
jwt.init_app(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

if __name__ == '__main__':
    app.run(debug=True, port=3001)
