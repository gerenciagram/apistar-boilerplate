from typing import List, Union, Dict
from datetime import datetime

from apistar.validators import Integer
from apistar.http import Host

from app.routes import route
from app.types import (
    Account, AccountId
)


#
# Account
#

from app.account import business as account_business


@route('GET', '/account')
def get_account() -> Account:
    """Get the logged in account."""
    return account_business.get_account(1)
