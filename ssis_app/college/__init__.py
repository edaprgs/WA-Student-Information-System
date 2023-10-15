from flask import Blueprint

college_bp = Blueprint('college',__name__)

from . import controller