from flask import Blueprint, render_template

error = Blueprint('error', __name__)

@error.app_errorhandler(404)
def handler_404(error):
    return render_template('errors/404.html', title='404'), 404