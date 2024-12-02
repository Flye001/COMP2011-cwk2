from flask import *
from flask_login import current_user, login_required
from datetime import datetime
from app.forms import ShiftForm
from app.helpers.dbHelper import DbHelper
from app.helpers.scheduleHelper import ScheduleHelper
from app.models import UserType

manager_bp = Blueprint("manager", __name__, url_prefix="/manager")

@manager_bp.before_request
@login_required
def set_global_values():
    g.role = "manager"

    user = DbHelper.get_user_by_id(current_user.get_id())

    if user == None:
        return redirect(url_for("login"))

    if (int(user.account_type) != UserType.MANAGER.value):
        return redirect(url_for("logout"))

@manager_bp.route("/")
def home():
    upcoming_shifts = [x for x in DbHelper.get_all_shifts() if x.end_time > datetime.now()]
    upcoming_shifts.sort(key=lambda x: x.end_time)
    all_users = DbHelper.get_all_users()
    unavailable_users = []
    for usr in all_users:
        for u in usr.unavailability:
            if u.start_time < datetime.now() and u.end_time > datetime.now():
                unavailable_users.append([usr, u.title])
                break
    return render_template("manager_pages/home.html",
                           shifts=upcoming_shifts[:3],
                           unavailable_users=unavailable_users,
                           active="home",
                           page_title="Welcome, " + current_user.name)

@manager_bp.route("/shifts")
def all_shifts():
    shifts = DbHelper.get_all_shifts()
    calendar_events = []
    for shift in shifts:
        calendar_events.append({
            "title": shift.title,
            "start": shift.start_time.isoformat(),
            "end": shift.end_time.isoformat(),
            "url": url_for("manager.manage_shift", id=shift.id)
        })
    return render_template("manager_pages/shifts.html",
                           shifts=calendar_events,
                           active="shifts",
                           page_title="All Shifts")

@manager_bp.route("/create-shift", methods=["GET", "POST"])
def create_shift():
    form = ShiftForm()
    if form.validate_on_submit():
        cont = True
        while cont:
            if form.start_date_time.data >= form.end_date_time.data:
                flash("Start date can not be after the end date!", "danger")
                break
            if form.workers_required.data < 1:
                flash(f"You must select at least 1 worker!", "danger")
                break
            result = DbHelper.create_shift(form.title.data,
                                        form.start_date_time.data,
                                        form.end_date_time.data,
                                        form.workers_required.data)
            if result != None:
                return redirect(url_for("manager.home"))
            else:
                flash("There was an error creating the shift!")
            cont = False

    return render_template("manager_pages/create_shift.html",
                           form=form,
                           active="shifts",
                           page_title="Create New Shift")

@manager_bp.route("/edit-shift", methods=["GET", "POST"])
def edit_shift():
    id = request.args.get("id")
    shift = DbHelper.get_shift_by_id(int(id))
    if shift == None:
        return redirect(url_for("error_404"))
    form = ShiftForm()
    if form.validate_on_submit():
        cont = True
        while cont:
            if form.start_date_time.data >= form.end_date_time.data:
                flash("Start date can not be after the end date!", "danger")
                break
            if form.workers_required.data < len(shift.workers):
                flash(f"You already have {len(shift.workers)} staff assigned. "
                "Please unassign staff before reducing this number!", "danger")
                break
            shift.title = form.title.data
            shift.start_time = form.start_date_time.data
            shift.end_time = form.end_date_time.data
            shift.workers_required = form.workers_required.data
            
            result = DbHelper.update_shift(shift.id, shift)
            if result != None:
                flash("Successfully updated the shift!", "success")
                return redirect(url_for("manager.manage_shift", id=shift.id))
            else:
                flash("There was an error updating the shift!", "danger")
            cont = False
    else:
        form.title.data = shift.title
        form.start_date_time.data = shift.start_time
        form.end_date_time.data = shift.end_time
        form.workers_required.data = shift.workers_required

    return render_template("manager_pages/edit_shift.html",
                           form=form,
                           active="shifts",
                           page_title="Edit Shift")

@manager_bp.route("/manage-shift")
def manage_shift():
    id = request.args.get("id")
    shift = DbHelper.get_shift_by_id(int(id))
    if shift == None:
        return redirect(url_for("error_404"))
    users = [x for x in DbHelper.get_all_users() if x.account_type == UserType.USER.value
                                                    and x not in shift.workers]
    
    available_users = []
    for usr in users:
        if ScheduleHelper.is_user_available(usr, shift):
            available_users.append(usr)
    return render_template("manager_pages/manage_shift.html",
                           shift=shift,
                           users=available_users,
                           active="shifts",
                           page_title="Manage Shift")

@manager_bp.route("/assign")
def assign_staff_to_shift():
    user_id = request.args.get("user_id")
    shift_id = request.args.get("shift_id")
    user = DbHelper.get_user_by_id(user_id)
    shift = DbHelper.get_shift_by_id(shift_id)

    if user == None or shift == None:
        return redirect(url_for("error_404"))

    if user in shift.workers:
        shift.workers.remove(user)
    else:
        if len(shift.workers) >= shift.workers_required:
            flash("The needed number of staff are already assigned!", "warning")
        elif not ScheduleHelper.is_user_available(user, shift):
            flash("The selected user is not available for this shift!", "warning")
        else:
            shift.workers.append(user)

    result = DbHelper.update_shift(shift_id, shift)
    if not result:
        flash("Error assigning the user to the shift!", "danger")
    
    return redirect(url_for("manager.manage_shift", id=shift_id))

@manager_bp.route("/delete-shift")
def delete_shift():
    id = request.args.get("id")
    result = DbHelper.delete_shift(id)
    if result:
        flash("Successfully deleted the shift!", "success")
    else:
        flash("Error deleting the shift!", "danger")
    return redirect(url_for("manager.home"))
