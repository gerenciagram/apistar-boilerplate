from typing import List, Union, Dict
from datetime import datetime

from apistar.validators import Integer
from apistar.http import Host

from app.routes import route
from app import types


#
# Account
#

from app.business import account as account_business


@route('GET', '/account')
def get_account() -> types.Account:
    """Get the logged in account."""
    return account_business.get_account(1)
