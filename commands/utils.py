import logging
import logging.config
import yaml
from pathlib import Path
from IPython.terminal.prompts import Prompts, Token
from traitlets.config import Config

from alembic.config import Config as AlembicConfig


def alembic_cfg():
    from app.environment import env

    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.set_section_option("alembic", "sqlalchemy.url", env['DB_URL'])
    return alembic_cfg


def configure_debug_logging():
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    with open(f'logging.yml', 'r') as log_config:
        config_yml = log_config.read()
        config_dict = yaml.load(config_yml)
        logging.config.dictConfig(config_dict)


def load_modules_wildcard(*module_names):
    module_name = ""
    for module_name in module_names:
        exec(compile(f"from {module_name} import *", "<file>", "exec"))

    del module_name, module_names
    return locals()


def load_modules(*module_names):
    modules = {}
    for module_name in module_names:
        modules[module_name] = __import__(module_name)

    return modules


def run_ipython_shell(project_name, banner, exit_msg='', domains=None):
    class CustomPrompt(Prompts):
        def in_prompt_tokens(self, cli=None):
            return [
                (Token.Prompt, f'{project_name} <'),
                (Token.PromptNum, str(self.shell.execution_count)),
                (Token.Prompt, '>: '),
            ]

        def out_prompt_tokens(self):
            return [
                (Token.OutPrompt, 'Out<'),
                (Token.OutPromptNum, str(self.shell.execution_count)),
                (Token.OutPrompt, '>: '),
            ]

    globals().update(load_modules('os', 'sys'))
    globals().update(load_modules_wildcard(*domains or []))

    cfg = Config()
    cfg.InteractiveShell.prompts_class = CustomPrompt
    cfg.InteractiveShell.confirm_exit = False

    from IPython.terminal.embed import InteractiveShellEmbed
    ipshell = InteractiveShellEmbed(
        config=cfg,
        banner1=banner,
        exit_msg=exit_msg
    )

    ipshell()
