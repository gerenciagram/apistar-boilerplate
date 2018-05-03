import logging

from functools import wraps
from typing import Any, Dict, List

from apistar import Route

from app.environment import env


logger = logging.getLogger(__name__)


routes: List[Route] = []


if env['DEBUG'] or env['TEST']:
    """routes.extend([
        Route('/docs', 'GET', api_documentation),
        Route('/{path}', 'GET', serve_static),
        Route('/schema/', 'GET', serve_schema),
        Route('/schema.js', 'GET', javascript_schema),
    ])"""


class RouteDecorator:

    def __init__(self,
                 method: str,
                 path: str,
                 name: str=None,
                 auth_required: bool=True,
                 **annotations: Dict[str, Any]):
        """
        Decorates a view function with routing facilities.

        :param method: HTTP verb to be used.
        :param path: URL endpoint.
        :param name: View name.
        :param auth_required: view requires authentication.
        :param kwargs: keyword arguments for the annotate decorator.
        """
        self.method = method
        self.path = path
        self.name = name
        self.auth_required = auth_required
        self.annotations = annotations

    def __call__(self, view):
        annotations = self.annotations
        if not self.auth_required:
            annotations['permissions'] = []

        @wraps(view)
        # @annotate(**annotations)
        def wrapped_view(*args, **kwargs):
            try:
                return {
                    # 'success': True,
                    'data': view(*args, **kwargs)
                }
            except Exception as exc:
                data = None
                if env['DEBUG']:
                    import traceback
                    data = ''.join(traceback.format_tb(exc.__traceback__))
                logger.exception("Unexpected Server Error")
                raise Exception(data)
        # FIXME override return may break schema and documentation
        wrapped_view.__annotations__['return'] = Dict[str, Any]
        routes.append(Route(self.path, self.method, wrapped_view, self.name))
        return wrapped_view


route = RouteDecorator

from app import views
