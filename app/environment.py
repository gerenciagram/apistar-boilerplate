import os

from apistar.validators import Boolean as BooleanValidator


NO_VALUE = object()


class Boolean(BooleanValidator):
    def validate(self, *args, **kwargs):
        return super().validate(allow_coerce=True, *args, **kwargs)


def var(cls, default=NO_VALUE, required=True):
    return type(cls.__name__, (cls,), {
        'default': default,
        'required': required
    })


class Environment(dict):

    def __init__(self, vars_dict):
        super().__init__()
        for key, var_func in vars_dict.items():
            value = self._resolve_value(key, var_func)
            if value is not NO_VALUE:
                self[key] = value

    def _resolve_value(self, key, var_func):
        value = NO_VALUE
        try:
            if hasattr(var_func, 'validate'):
                value = var_func().validate(os.environ[key])
            else:
                value = var_func(os.environ[key])
        except KeyError:
            if hasattr(var_func, 'default'):
                value = var_func.default() if callable(var_func.default) else var_func.default

        required = getattr(var_func, 'required', True)
        if value is NO_VALUE and required:
            raise Exception(f'{key} variable not found in environment')

        return value


env = Environment({

    #
    # Debugging and testing
    #

    'DEBUG': var(Boolean, default=False),
    'TEST': var(Boolean, default=False),
})


if env['DEBUG']:
    import builtins, pdb, pprint
    setattr(builtins, 'pprint', pprint.pprint)
    setattr(builtins, 'breakpoint', pdb.set_trace)
