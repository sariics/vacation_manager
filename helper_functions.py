from datetime import date
from functools import wraps
from flask import request, make_response
from db_service import check_user_credentials


def get_vacation_date_limits():
    current_date = date.today()
    date_min = str(current_date)
    date_max = current_date.replace(year=current_date.year + 1)
    return date_min, date_max


# authentication decorator
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if check_user_credentials(name=auth.username, password=auth.password):

            return f(*args, **kwargs)
        return make_response(
            "Could not verify user credentials!",
            401,
            {"WWW-Authenticate": "Basic realm=Login Requried"},
        )

    return decorated
