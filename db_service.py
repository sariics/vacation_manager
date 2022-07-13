from pymongo import MongoClient
from datetime import datetime
from typing import Union

db_connection_string = "mongodb://localhost:27017/"
client: MongoClient = MongoClient(db_connection_string)

if "vacation_management" not in client.list_database_names():
    db = client["vacation_management"]
    employee_vacation = db["employee_vacation"]
else:
    db = client.vacation_management
    employee_vacation = db.employee_vacation
    employee_vacation.delete_many({})
# employee_vacation.create_index(["name", pymongo.DESCENDING]) # create index for employee name,


def create_database():

    user_entry_examples = [
        {
            "name": "Jane Doe",
            "password": "Jane123",
            "vac_current_year": 30,
            "vac_leftover_last_year": 3,
            "vac_remaining_current": 25,
            "requested_leave_total": 8,
            "vacation_requests": [
                {
                    "request_id": 1,
                    "vacation_start": datetime(year=2022, month=7, day=4),
                    "vacation_end": datetime(year=2022, month=7, day=8),
                    "requested_leave": 3,
                    "special_leave": False,
                    "request_submitted": True,
                    "request_approved": True,
                },
                {
                    "request_id": 2,
                    "vacation_start": datetime(year=2022, month=8, day=15),
                    "vacation_end": datetime(year=2022, month=8, day=19),
                    "requested_leave": 5,
                    "special_leave": False,
                    "request_submitted": True,
                    "request_approved": False,
                },
            ],
        },
        {
            "name": "Bilbo Beutlinn",
            "password": "Bilbo123",
            "vac_current_year": 30,
            "vac_leftover_last_year": 0,
            "vac_remaining_current": 25,
            "requested_leave_total": 5,
            "vacation_requests": [
                {
                    "request_id": 1,
                    "vacation_start": datetime(year=2022, month=7, day=4),
                    "vacation_end": datetime(year=2022, month=7, day=8),
                    "requested_leave": 3,
                    "special_leave": False,
                    "request_submitted": True,
                    "request_approved": False,
                }
            ],
        },
        {
            "name": "Arno Duebel",
            "password": "Arno123",
            "vac_current_year": 30,
            "vac_leftover_last_year": 4,
            "vac_remaining_current": 34,
            "requested_leave_total": 0,
            "vacation_requests": [],
        },
    ]
    employee_vacation.insert_many(user_entry_examples)


def get_user_data(user: str) -> dict:
    user_data: dict = employee_vacation.find_one(
        {"name": user}, {"vac_current_year": 0, "vac_leftover_last_year": 0}
    )
    return user_data


def check_user_credentials(name: str, password: str) -> Union[str, bool]:
    if employee_vacation.find_one({"name": name, "password": password}):
        return name
    return False


def add_request_to_db(name: str, request: dict, vac_days: int):

    employee_vacation.update_one(
        {"name": name}, {"$push": {"vacation_requests": request}}
    )
    employee_vacation.update_one(
        {"name": name}, {"$inc": {"requested_leave_total": vac_days}}
    )
    employee_vacation.update_one(
        {"name": name}, {"$inc": {"vac_remaining_current": -vac_days}}
    )  # join both


def count_total_user_requests(name: str):
    return list(
        employee_vacation.aggregate(
            [
                {
                    "$project": {
                        "name": name,
                        "request_count": {"$size": "$vacation_requests"},
                    }
                }
            ]
        )
    )[0]["request_count"]


def delete_user_vac_request(name: str, request_id: int):
    employee_vacation.update_one(
        {"name": name}, {"$pull": {"vacation_requests": {"request_id": request_id}}}
    )
