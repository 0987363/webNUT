from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPNotFound

from .basic_auth import BasicAuthMiddleware
from .settings import load_config


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('ups_view', '/{ups}')
    config.add_view('webnut.views.notfound',
            renderer='webnut:templates/404.pt',
            context='pyramid.exceptions.NotFound')
    config.scan()
    app = config.make_wsgi_app()
    nut_config = load_config()
    return BasicAuthMiddleware(app, nut_config.webnut_username, nut_config.webnut_password)
