from flask import Blueprint
from flasgger import Swagger

from src.controller.ocrController import upload_image

#region Tanvir
automation_print = Blueprint('automation_print', __name__)

automation_print.route('/upload_image', methods=['POST'])(upload_image)