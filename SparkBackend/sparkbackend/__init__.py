import sys
from pyramid.config import Configurator
from sparkbackend.handler.CitationHandler import CitationHandler
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from sparkbackend.security import groupfinder


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    authn_policy = AuthTktAuthenticationPolicy(
        'sosecret', callback=groupfinder)
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings,
                          root_factory='sparkbackend.models.models.RootFactory',
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy)
    config.add_static_view('static', 'sparkbackend:static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('citation', '/citation/{id}')
    config.add_route('citation_index', '/citation/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.add_view(CitationHandler, attr='citation_get', route_name='citation',request_method='GET')
    config.add_view(CitationHandler, attr='citation_index', route_name='citation_index',request_method='GET')
    config.add_view(CitationHandler, attr='citation_post', route_name='citation_index',request_method='POST')
    config.add_view(CitationHandler, attr='citation_put', route_name='citation',request_method='PUT',permission='edit')
    config.add_view(CitationHandler, attr='citation_delete', route_name='citation',request_method='DELETE',permission='edit')

    config.add_view('sparkbackend.login.login', route_name='login', renderer='sparkbackend:templates/login.pt')
    config.add_view('sparkbackend.login.logout', route_name='logout')
    config.add_view('sparkbackend.login.login',context='pyramid.httpexceptions.HTTPForbidden',renderer='sparkbackend:templates/login.pt')


    config.scan()
    return config.make_wsgi_app()

