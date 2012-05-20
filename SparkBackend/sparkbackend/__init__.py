import sys

from pyramid.config import Configurator
from sparkbackend.handler.CitationHandler import CitationHandler

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
#    engine = engine_from_config(settings, 'sqlalchemy.')
#    DBSession.configure(bind=engine)
    config = Configurator(settings=settings)
#    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('citation', '/citation/{id}')
    config.add_route('citation_index', '/citation/')
    config.add_view(CitationHandler, attr='citation_get', route_name='citation',request_method='GET')
    config.add_view(CitationHandler, attr='citation_index', route_name='citation_index',request_method='GET')
    config.add_view(CitationHandler, attr='citation_post', route_name='citation_index',request_method='POST')
    config.add_view(CitationHandler, attr='citation_put', route_name='citation',request_method='PUT')
    config.add_view(CitationHandler, attr='citation_delete', route_name='citation',request_method='DELETE')

    config.scan()
    return config.make_wsgi_app()

