from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from extensions import db
from routes.report_routes import report_bp
from routes.expense_routes import expense_bp
from routes.ai_routes import ai_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)

    # routes
    app.register_blueprint(expense_bp, url_prefix="/expense")
    app.register_blueprint(ai_bp, url_prefix="/ai")
    app.register_blueprint(report_bp, url_prefix="/report")

    @app.route("/")
    def home():
        return jsonify({
            "message": "FinTrack AI Running 🚀",
            "status": "active"
        })

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)