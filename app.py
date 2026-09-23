from flask import Flask, render_template
from config import Config
from models import db
from routes.auth import auth_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
app.register_blueprint(auth_bp)

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
