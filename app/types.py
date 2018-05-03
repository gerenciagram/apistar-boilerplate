from apistar import types, validators


class Account(types.Type):
    account_id = validators.Integer()
    email = validators.String(max_length=200)
    first_name = validators.String(max_length=100)

class AccountId(types.Type):
    id = validators.Integer()
