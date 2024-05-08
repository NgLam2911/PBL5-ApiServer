from flask import Flask, render_template
from app import app as web_app
from api import app as api_app

app = Flask(__name__)

# Apply for all routes
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.register_blueprint(web_app)
    app.register_blueprint(api_app)
    app.run(debug=True, host="0.0.0.0", port=80, use_reloader=False)
    # Prevent reload to avoid memory leak