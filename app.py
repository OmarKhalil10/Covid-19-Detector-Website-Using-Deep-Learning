from flask import Flask, request, render_template, redirect, abort, jsonify
from flask_cors import CORS
from sqlalchemy import or_


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    #setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route("/")
    def landing_page():
        return render_template("pages/index.html")
    
    @app.route("/about")
    def about_page():
        return render_template("pages/about.html")
    
    @app.route("/contact")
    def contact_page():
        return render_template("pages/contact.html")

    @app.route("/faq")
    def faq_page():
        return render_template("pages/faq.html")
    
    @app.route("/prevention")
    def prevention_page():
        return render_template("pages/prevention.html")

    @app.route("/search")
    def search_page():
        return render_template("pages/search.html")

    @app.route("/symptom")
    def symptom_page():
        return render_template("pages/symptom.html")
   
    @app.route("/symptom-checker")
    def symptom_checker_page():
        return render_template("pages/symptom-checker.html")

    @app.route("/virus-checker")
    def virus_checker_page():
        return render_template("pages/virus-checker.html")

    @app.route("/tracker")
    def tracker_page():
        return render_template("pages/tracker.html")

    

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return render_template('/pages/error.html', data={
            'success': False,
            'error': 404,
            'description': 'Sorry but the page you are looking for does not exist, have been removed, name changed or is temporarily unavailable.',
            'message': 'Page Not Be Found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server errors'
        }), 500
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4040, debug=True)