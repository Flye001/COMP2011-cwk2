from flask import *
from datetime import datetime
from flask_login import current_user, login_required
from app.forms import UnavailabilityForm
from app.helpers.dbHelper import DbHelper
from app.helpers.scheduleHelper import ScheduleHelper
from app.models import Unavailability, UserType

user_bp = Blueprint("user", __name__, url_prefix="/user")

@user_bp.before_request
@login_required
def set_global_values():
    g.role = "user"

    user = DbHelper.get_user_by_id(current_user.get_id())

    if user == None:
        return redirect(url_for("login"))

    if (int(user.account_type) != UserType.USER.value):
        return redirect(url_for("logout"))

@user_bp.route("/")
def home():
    user = DbHelper.get_user_by_id(current_user.get_id())
    shifts = user.shifts
    calendar_events = []
    for shift in shifts:
        calendar_events.append({
            "title": f"{shift.title}",
            "start": shift.start_time.isoformat(),
            "end": shift.end_time.isoformat(),
            "url": url_for("user.view_shift", id=shift.id)
        })

    unavailability = [x for x in user.unavailability if x.end_time > datetime.now()]
    unavailability.sort(key=lambda x: x.start_time)
    
    return render_template("user_pages/home.html", 
                           calendar_events=calendar_events,
                           unavailability=unavailability[:5],
                           active="home",
                           page_title="Welcome, " + current_user.name)

@user_bp.route("/schedule")
def schedule():
    shifts = DbHelper.get_user_by_id(current_user.get_id()).shifts
    calendar_events = []
    for shift in shifts:
        calendar_events.append({
            "title": shift.title,
            "start": shift.start_time.isoformat(),
            "end": shift.end_time.isoformat(),
            "url": url_for("user.view_shift", id=shift.id)
        })
    return render_template("user_pages/schedule.html", 
                           calendar_events=calendar_events,
                           active="schedule",
                           page_title="Your Schedule")

@user_bp.route("/unavailable", methods=["GET", "POST"])
def unavailable():
    user = DbHelper.get_user_by_id(current_user.get_id())
    form = UnavailabilityForm()
    if form.validate_on_submit():
        cont = True
        while cont:
            if form.start_date_time.data >= form.end_date_time.data:
                flash("Start date cannot be after the end date!", "danger")
                break
            if not ScheduleHelper.verify_new_unavailability(form.start_date_time.data, form.end_date_time.data, user):
                flash("Cannot add this unavailability - it clashes with one of your shifts.", "danger")
                break
            result = DbHelper.create_unavailability(form.title.data,
                                        form.start_date_time.data,
                                        form.end_date_time.data)
            if result != None:
                flash("Successfully added your unavailability!", "success")
                form = UnavailabilityForm(formdata=None)
            else:
                flash("There was an error adding the unavailability!", "danger")
            cont = False

    user = DbHelper.get_user_by_id(current_user.get_id())

    unavailable_dates = []
    for u in [x for x in user.unavailability if x.end_time > datetime.now()]:
        unavailable_dates.append(
        {
            "title": u.title,
            "start": u.start_time.isoformat(),
            "end": u.end_time.isoformat(),
            "url": url_for("user.edit_unavailability", id=u.id)
        })
    
    return render_template("user_pages/unavailable.html",
                           unavailable_dates=unavailable_dates,
                           form=form,
                           active="unavailable",
                           page_title="Your Unavailability")

@user_bp.route("/edit-unavailability", methods=["GET", "POST"])
def edit_unavailability():
    id = request.args.get("id")
    user = DbHelper.get_user_by_id(current_user.get_id())
    unavail = DbHelper.get_unavailability_by_id(id)
    if unavail == None:
        return redirect(url_for("error_404"))
    form = UnavailabilityForm()
    if form.validate_on_submit():
        cont = True
        while cont:
            if form.start_date_time.data >= form.end_date_time.data:
                flash("Start date cannot be after the end date!", "danger")
                break
            if not ScheduleHelper.verify_new_unavailability(form.start_date_time.data, form.end_date_time.data, user):
                flash("Cannot add this unavailability - it clashes with one of your shifts.", "danger")
                break
            unavail.title = form.title.data
            unavail.start_time = form.start_date_time.data
            unavail.end_time = form.end_date_time.data
            result = DbHelper.update_unavailability(id, unavail)
            if result != None:
                flash("Successfully updated your unavailability!", "success")
            else:
                flash("There was an error updating the unavailability!", "danger")
            cont = False

    else:
        form.title.data = unavail.title
        form.start_date_time.data = unavail.start_time
        form.end_date_time.data = unavail.end_time
    
    return render_template("user_pages/edit_unavailability.html",
                           form=form,
                           id=id,
                           active="unavailable",
                           page_title="Edit Unavailability")

@user_bp.route("/delete-unavailability")
def delete_unavailability():
    id = request.args.get("id")
    result = DbHelper.delete_unavailability(id)
    if result:
        flash("Successfully deleted the unavailability!", "success")
    else:
        flash("Error deleting the unavailability!", "danger")
    return redirect(url_for("user.home"))

@user_bp.route("/shift")
def view_shift():
    shift_id = request.args.get("id")
    shift = DbHelper.get_shift_by_id(shift_id)
    if shift == None:
        return redirect(url_for("error_404"))
    return render_template("user_pages/view_shift.html",
                           shift=shift,
                           page_title=shift.title)