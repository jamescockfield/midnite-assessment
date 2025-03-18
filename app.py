from flask import Flask, jsonify
from database.database import init_db, db
from app.routes import event_bp
from dependencies import init_dependencies

# Initialize the app
app = Flask(__name__)

# Initialize the database
init_db(app)

# Register blueprints
app.register_blueprint(event_bp)

# Initialize the DI framework
init_dependencies(app)

# Request middleware and error handlers
@app.teardown_request
def teardown_request(exception=None):
    if exception:
        db.session.rollback()
    else:
        db.session.commit()
    db.session.remove()

@app.errorhandler(ValueError)
def handle_validation_error(error):
    return jsonify({"error": str(error)}), 400

@app.errorhandler(Exception)
def handle_generic_error(error):
    print(error)
    return jsonify({"error": "Internal server error"}), 500

# Run the server
if __name__ == '__main__':
    app.run(debug=True, port=5000)
