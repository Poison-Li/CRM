from flask import Blueprint

bp = Blueprint("trade", __name__)

from app.trade import api