from app.db import db
from app import models
from sqlalchemy.exc import SQLAlchemyError
from flask_login import current_user
import bcrypt

# CRUD operations for db tables
class DbHelper:
    @staticmethod
    def create_user(email, fname, lname, account_type, password):
        hashed_pwd = bcrypt.hashpw(bytes(password, "utf-8"), bcrypt.gensalt(rounds=12))
        try:
            user = models.User(
                email=email,
                fname=fname,
                lname=lname,
                account_type=account_type,
                password_hash=hashed_pwd,
                is_active=True,
                is_anonymous=False,
                is_authenticated=False
            )
            db.session.add(user)
            db.session.commit()
            return user
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Error creating user:", e)
            return None

    @staticmethod
    def get_user_by_id(user_id):
        try:
            user = models.User.query.get(user_id)
            return user
        except SQLAlchemyError as e:
            print("Error retrieving user:", e)
            return None
        
    @staticmethod
    def get_user_by_email(user_email):
        try:
            user = models.User.query.filter_by(email=user_email).first()
            return user
        except SQLAlchemyError as e:
            print("Error retrieving user by email:", e)
            return None

    @staticmethod
    def get_all_users():
        try:
            users = models.User.query.all()
            return users
        except SQLAlchemyError as e:
            print("Error retrieving all users:", e)
            return None

    @staticmethod
    def update_user(user_id, updated_user :models.User):
        try:
            user :models.User = models.User.query.get(user_id)
            if not user:
                print("User not found")
                return None
            
            user = updated_user

            db.session.commit()
            return user
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Error updating user:", e)
            return None

    @staticmethod
    def delete_user(user_id):
        try:
            user = models.User.query.get(user_id)
            if not user:
                print("User not found")
                return False

            db.session.delete(user)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Error deleting user:", e)
            return False
        
    @staticmethod
    def create_shift(name, start, end, workers):
        try:
            shift = models.Shift(
                title=name,
                start_time=start,
                end_time=end,
                workers_required=workers,
                creating_user_id=current_user.id
            )
            db.session.add(shift)
            db.session.commit()
            return shift
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Error creating shift:", e)
            return None

    @staticmethod
    def get_all_shifts():
        try:
            shifts = models.Shift.query.all()
            return shifts
        except SQLAlchemyError as e:
            print("Error retrieving all shifts:", e)
            return None

    @staticmethod
    def get_shift_by_id(shift_id):
        try:
            shift = models.Shift.query.get(shift_id)
            return shift
        except SQLAlchemyError as e:
            print("Error retrieving shift:", e)
            return None
        
    @staticmethod
    def update_shift(shift_id, updated_shift :models.Shift):
        try:
            shift :models.Shift = models.Shift.query.get(shift_id)
            if not shift:
                print("Shift not found")
                return None
            
            shift = updated_shift

            db.session.commit()
            return shift
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Error updating shift:", e)
            return None

    @staticmethod
    def delete_shift(shift_id):
        try:
            shift = models.Shift.query.get(shift_id)
            if not shift:
                print("Shift not found")
                return False

            db.session.delete(shift)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Error deleting shift:", e)
            return False

    @staticmethod
    def create_unavailability(name, start, end):
        try:
            unavail = models.Unavailability(
                title=name,
                start_time=start,
                end_time=end,
                user_id=current_user.id
            )
            db.session.add(unavail)
            db.session.commit()
            return unavail
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Error creating unavailability:", e)
            return None

    @staticmethod
    def get_all_unavailability():
        try:
            unavail = models.Unavailability.query.all()
            return unavail
        except SQLAlchemyError as e:
            print("Error retrieving all unavailability:", e)
            return None

    @staticmethod
    def get_unavailability_by_id(unavail_id):
        try:
            unavail = models.Unavailability.query.get(unavail_id)
            return unavail
        except SQLAlchemyError as e:
            print("Error retrieving unavailability:", e)
            return None
        
    @staticmethod
    def update_unavailability(unavail_id, updated_unavail :models.Unavailability):
        try:
            unavail :models.Unavailability = models.Unavailability.query.get(unavail_id)
            if not unavail:
                print("Unavailability not found")
                return None
            
            unavail = updated_unavail

            db.session.commit()
            return unavail
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Error updating unavailability:", e)
            return None

    @staticmethod
    def delete_unavailability(unavail_id):
        try:
            unavail = models.Unavailability.query.get(unavail_id)
            if not unavail:
                print("Unavailability not found")
                return False

            db.session.delete(unavail)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Error deleting unavailability:", e)
            return False
