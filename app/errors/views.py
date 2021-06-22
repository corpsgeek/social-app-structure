from flask import render_template, url_for

from . import errors


@errors.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html')


@errors.app_errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html')