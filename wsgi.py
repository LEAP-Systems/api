# -*- coding: utf-8 -*-
from app import init_app
from flask import jsonify, redirect, url_for

app = init_app()


@app.errorhandler(404)
def resource_not_found(err):
    return jsonify(error=str(err)), 404

@app.errorhandler(Exception)
def internal_error(err):
    response = {
        'success': False,
        'error': {
            'type': 'UncaughtException',
            'message': err
        }
    }
    return jsonify(response), 500

@app.route("/")
def redirect_to_latest_api_version():
    """Redirects to /v1"""
    return redirect(url_for("api.root"), code=302)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
