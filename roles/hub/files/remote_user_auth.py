import os
from jupyterhub.handlers import BaseHandler
from jupyterhub.auth import Authenticator, LocalAuthenticator
from jupyterhub.utils import url_path_join
from tornado import gen, web
from traitlets import Unicode


class RemoteUserLoginHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        username = yield self.authenticator.get_authenticated_user(self, None)

        if username:
            user = self.user_from_username(username)
            self.set_login_cookie(user)
            self.redirect(url_path_join(self.hub.server.base_url, 'home'))
        else:
            raise web.HTTPError(403)

class RemoteUserAuthenticator(Authenticator):
    """
    Accept the authenticated user name from the REMOTE_USER HTTP header.
    """
    header_name = Unicode(
        default_value='Remote-User',
        config=True,
        help="""HTTP header to inspect for the authenticated username.""")

    def get_handlers(self, app):
        return [
            (r'/login', RemoteUserLoginHandler),
        ]

    @gen.coroutine
    def authenticate(self, handler, data=None):
        remote_user = handler.request.headers.get(self.header_name, "")
        if remote_user == "":
            raise web.HTTPError(401)
        else:
            return remote_user.split("@")[0]

    def logout_url(self, base_url):
        """
        There is nowhere to log out, so point to /.
        """
        return '/'


class LocalRemoteUserAuthenticator(LocalAuthenticator, RemoteUserAuthenticator):

    """A version that mixes in local system user creation"""
    pass
