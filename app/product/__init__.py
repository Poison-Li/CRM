from flask import Blueprint

bp = Blueprint("product", __name__, static_url_path='/fsd', static_folder='/sdsd')

from app.product import api