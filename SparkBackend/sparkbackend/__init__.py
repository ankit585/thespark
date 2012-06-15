import sys
from pyramid.config import Configurator
from sparkbackend.handler.CitationHandler import CitationHandler
from sparkbackend.handler.UserHandler import UserHandler
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

    config.add_route('citation', '/api/v1/citation/{id}')
    config.add_route('citation_index', '/api/v1/citation/')

    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    # V1 User API
    config.add_route('user_index', '/api/v1/user/')
    config.add_route('user', '/api/v1/user/{userID}')
    config.add_route('user_email', '/api/v1/user/email/{email}')

    config.add_view(CitationHandler, attr='citation_get', route_name='citation',request_method='GET',permission='view')
    config.add_view(CitationHandler, attr='citation_index', route_name='citation_index',request_method='GET',permission='view')
    config.add_view(CitationHandler, attr='citation_post', route_name='citation_index',request_method='POST',permission='view')
    config.add_view(CitationHandler, attr='citation_put', route_name='citation',request_method='PUT',permission='view')
    config.add_view(CitationHandler, attr='citation_delete', route_name='citation',request_method='DELETE',permission='view')


    config.add_view(UserHandler,attr='user_login', route_name='login',renderer='sparkbackend:templates/login.pt',permission='view')
    config.add_view(UserHandler,attr='user_logout', route_name='logout',request_method='GET',permission='view')
    config.add_view(UserHandler,attr='user_get', route_name='user',request_method='GET',permission='view')
    config.add_view(UserHandler,attr='user_email_get', route_name='user_email',request_method='GET',permission='view')
    config.add_view(UserHandler,attr='register', route_name='user_index',request_method='POST',permission='view')
    config.add_view(UserHandler,attr='reset_password', route_name='user',request_method='PUT',permission='view')
    config.add_view(UserHandler,attr='user_delete', route_name='user',request_method='DELETE',permission='view')
   # config.add_view('sparkbackend.login.login',context='pyramid.httpexceptions.HTTPForbidden',renderer='sparkbackend:templates/login.pt')


    config.scan()
    return config.make_wsgi_app()

