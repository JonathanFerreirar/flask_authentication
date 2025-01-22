from utils.extentions import bcrypt, jwt
from config import create_app

app = create_app()
bcrypt.init_app(app)
jwt.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, port=3001)
