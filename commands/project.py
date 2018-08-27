
from pathlib import Path
from dotenv import load_dotenv

from commands.utils import (
    load_modules_wildcard, configure_debug_logging
)


class Cli:

    project_name = "python-web-app-boilerplate"
    domains = [
        'app.environment',

        # add your automatic imports here
    ]

    def __init__(self, env_name='local'):
        configure_debug_logging()

        load_dotenv(dotenv_path=Path('.') / f'env/base.env')
        load_dotenv(dotenv_path=Path('.') / f'env/{env_name}.env', verbose=True, override=True)

    def shell(self):
        from commands.utils import run_ipython_shell
        from app.environment import env

        return run_ipython_shell(
            project_name=self.project_name,
            banner=f'*** Welcome to {self.project_name} shell ***',
            domains=self.domains
        )

    def run(self, host='0.0.0.0', port=5000, debug=True):
        from app import app
        app.serve(
            host=host,
            port=port,
            debug=debug
        )

    def app(self):
        from gunicorn.app.wsgiapp import WSGIApplication
        WSGIApplication().run()

    def migrate(self, version="head"):
        from alembic import command
        from commands.utils import alembic_cfg
        command.upgrade(alembic_cfg(), version)

    def downgrade(self, version="head"):
        from alembic import command
        from commands.utils import alembic_cfg
        command.downgrade(alembic_cfg(), version)

    def makemigrations(self, message=None, autogenerate=True):
        from alembic import command
        from commands.utils import alembic_cfg
        command.revision(alembic_cfg(), message=message, autogenerate=autogenerate)
        
    def createuser(self, username, password):
        pass
        
    def deploy(self):
        pass

