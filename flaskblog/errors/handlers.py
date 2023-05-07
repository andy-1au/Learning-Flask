from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

# default value for return is 200, so we didn't need to do it for our other routes
# but for errors, we must specify it
# app_errorhandler instead of errorhandler because we need it to work across the entire app

@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500

