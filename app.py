from db_service import (
    create_database,
    add_request_to_db,
    get_user_data,
    count_total_user_requests,
    delete_user_vac_request,
    check_user_credentials,
)
from helper_functions import get_vacation_date_limits, auth_required
from flask import Flask, render_template, request, redirect, url_for, make_response
from datetime import datetime


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/vacation_management"


create_database()


@app.route("/")
def home() -> render_template:
    auth = request.authorization
    user = check_user_credentials(name=auth.username, password=auth.password)
    if user:
        user_data = get_user_data(user)
        all_requests = user_data["vacation_requests"]
        pending_requests = [
            dict for dict in all_requests if dict["request_approved"] == False
        ]
        approved_requests = [
            dict for dict in all_requests if dict["request_approved"] == True
        ]
        date_min, date_max = get_vacation_date_limits()
        return render_template(
            "home.html",
            name=user_data["name"],
            requested_total=user_data["requested_leave_total"],
            remaining=user_data["vac_remaining_current"],
            pending=pending_requests,
            approved=approved_requests,
            today=date_min,
            date_max=date_max,
        )
    return make_response(
        "Could not verify user credentials!",
        401,
        {"WWW-Authenticate": "Basic realm=Login Requried"},
    )


# User können neue Urlaubsanträge stellen
@app.route("/add_request", methods=["POST"])
@auth_required
def add_request() -> redirect:
    user = request.form.get("username")
    start_date = datetime.strptime(request.form.get("startdate"), "%Y-%m-%d")
    end_date = datetime.strptime(request.form.get("enddate"), "%Y-%m-%d")
    special_leave = True if request.form.get("specialleave") else False
    requested_vac_days = (end_date - start_date).days + 1

    requests_count = count_total_user_requests(name=user)
    new_request = {
        "request_id": requests_count + 1,
        "vacation_start": start_date,
        "vacation_end": end_date,
        "requested_leave": requested_vac_days,
        "special_leave": special_leave,
        "request_submitted": True,
        "request_approved": False,
    }

    add_request_to_db(request=new_request, name=user, vac_days=requested_vac_days)
    return redirect(url_for("home"))


# User können Urlaubsanträge löschen, solange sie noch nicht genehmigt sind
@app.route("/delete/<int:request_id>")
@auth_required
def delete(request_id) -> redirect:
    user = request.args.get("name")
    delete_user_vac_request(name=user, request_id=request_id)

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
