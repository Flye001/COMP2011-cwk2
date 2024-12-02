# Useful functions for scheduling
from datetime import datetime
from app.models import Shift, Unavailability, User


class ScheduleHelper():
    @staticmethod
    def is_clash(u :Unavailability, s :Shift) -> bool:
        if u.end_time >= s.start_time and s.end_time >= u.start_time:
                return True
        
    @staticmethod
    def is_clash_time(start :datetime, end :datetime, s :Shift) -> bool:
        if end >= s.start_time and s.end_time >= start:
                return True

    @staticmethod
    def is_user_available(user :User, shift :Shift) -> bool:
        for u in user.unavailability:
            if ScheduleHelper.is_clash(u, shift):
                 return False
        for s in user.shifts:
             if ScheduleHelper.is_clash_time(s.start_time, s.end_time, shift):
                  return False
        return True
    
    @staticmethod
    def verify_new_unavailability(start_time :datetime, end_time :datetime, user :User) -> bool:
        for s in user.shifts:
             if ScheduleHelper.is_clash_time(start_time, end_time, s):
                  return False
        return True