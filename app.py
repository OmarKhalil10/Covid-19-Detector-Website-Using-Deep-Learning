import os
from flask import Flask, request, render_template, redirect, abort, jsonify, flash, url_for
from flask_cors import CORS
from flask_mail import Mail, Message
from sqlalchemy import or_
import numpy as np
import tensorflow as tf
from werkzeug.utils import secure_filename
from flask import send_from_directory
from keras.preprocessing import image
import matplotlib.pyplot as plt

UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
SECRET_KEY=os.environ.get('SECRET_KEY')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
PASSWORD = os.environ.get('GMAIL_APP_PASSWORD')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SECRET_KEY'] = SECRET_KEY
    #setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'johnaziz269@gmail.com',
    MAIL_PASSWORD = PASSWORD,
    ))

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

    @app.route("/prediction", methods=["POST", "GET"])
    def prediction_page():
        # check if the post request has the file part
        if request.method == 'POST':
            if 'files' not in request.files:
                flash('No file part')
            file = request.files['files']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            model =  tf.keras.models.load_model('.\\covid_classifier_model.h5')
            
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            img = image.load_img(path, target_size=(200, 200))
            x=image.img_to_array(img)
            x /= 255
            x=np.expand_dims(x, axis=0)
            images = np.vstack([x])
            
            classes = model.predict(images, batch_size=10)
            percentage = round(classes[0][0] * 100, 2)
            if classes[0]>0.5:
                prediction = "Positive"
            else:
                prediction = "Negative"
                percentage = 100 - percentage
            return jsonify({
                'prediction': prediction,
                'success': True,
                'percentage': percentage
                }), 200
        return jsonify({
                'success': False
                }), 405

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'],
                                filename)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return render_template('/pages/errors/error.html', data={
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