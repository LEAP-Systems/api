# -*- coding: utf-8 -*-
from app import init_app
from flask import jsonify, redirect, url_for
from config import Config

app = init_app(Config)


@app.errorhandler(404)
def resource_not_found(err):
    return jsonify(error=str(err)), 404

@app.errorhandler(Exception)
def internal_error(err):
    # log the exception stack trace
    app.logger.exception(err)
    # create hr error message for response payload
    message = [str(x) for x in err.args]
    response = {
        'success': False,
        'error': {
            'type': err.__class__.__name__,
            'message': message
        }
    }
    return jsonify(response), 500

@app.route("/")
def redirect_to_latest_api_version():
    """Redirects to /v1"""
    return redirect(url_for("api.root"), code=302)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
