import logging
from IPython.terminal.prompts import Prompts, Token
from traitlets.config.loader import Config


def configure_debug_logging():
    logging.basicConfig(level='DEBUG')
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


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
