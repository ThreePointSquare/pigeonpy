from functools import wraps
from flask import request, redirect, url_for
from flask_restful import Resource, abort

from pigeonpie import app, session
from pigeonpie.forge import ForgeUser


#############################
# AUTHENTICATION END POINTS #
#############################

@app.route('/api/callback')
def callback_authentication():
    """ Authentication endpoint """
    code = request.args.get('code')
    target = request.args.get('state', '/')
    if not ForgeUser.login(code=code):
        code = 401
    return redirect(target)

@app.route('/user/logout')
def logout():
    """ Authentication endpoint """
    ForgeUser.logout()
    return redirect(url_for('index'))

#############################
# AUTHENTICATION DECORATORS #
#############################

def require_admin(func):
    """ Secure method decorator """
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = session.get('user')
        if user and user['userId'] == '200809200314193' or app.testing is True:
            app.logger.info('Admin Resource: User is Authenticated > {}'.format(request.url))
            return func(*args, **kwargs)
        app.logger.info('Unauthorized.')
        abort(401)
    return wrapper

def require_user(func):
    """ Secure method decorator """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('access_token') or app.testing is True:
            app.logger.info('Securer Resource: User is Authenticated > {}'.format(request.url))
            return func(*args, **kwargs)

        app.logger.info('Unauthorized Resource.')
        abort(401)
    return wrapper


class UserResouce(Resource):
    method_decorators = [require_user]

class AdminResource(Resource):
    method_decorators = [require_admin]