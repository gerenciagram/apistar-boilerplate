from apistar import App as ApistarApp
from apistar_cors import CORSMixin

from app.routes import routes


class App(CORSMixin, ApistarApp):
    pass


def homepage() -> dict:
    return {
        'message': 'home'
    }


app = App(
    routes=routes
)
