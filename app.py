from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
import urllib3
import logging
import sys
from src.routes.ocrRoutes import automation_print
from flask import redirect

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    logging.basicConfig(filename='app.log', level=logging.DEBUG)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logging.getLogger().addHandler(console_handler)

    app.register_blueprint(automation_print, url_prefix='/api')
    return app

app = create_app()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
swagger = Swagger(app, template_file='apidocs/swagger.yml')
@app.route('/')
def root():
    return redirect('/apidocs/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)