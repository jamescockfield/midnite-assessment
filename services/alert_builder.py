from datetime import timedelta
from repositories import UserActivityRepository
from domain_types import ActivityType, AlertCode
from database.models import UserActivity

class AlertBuilder:
    def __init__(self, activity_repository: UserActivityRepository):
        self.activity_repository = activity_repository

    def build_alerts(self, activity: UserActivity):
        alert_codes = []
        
        if activity.activity_type == ActivityType.WITHDRAW.value and activity.amount > 100:
            alert_codes.append(AlertCode.LARGE_WITHDRAWAL.value)
        if self.check_consecutive_withdraws(activity.user_id):
            alert_codes.append(AlertCode.CONSECUTIVE_WITHDRAWALS.value)
        if self.check_increasing_deposits(activity.user_id):
            alert_codes.append(AlertCode.INCREASING_DEPOSITS.value)
        if self.check_accumulative_deposit(activity.user_id):
            alert_codes.append(AlertCode.ACCUMULATIVE_DEPOSIT.value)
            
        return alert_codes

    def check_consecutive_withdraws(self, user_id):
        activities = self.activity_repository.get_user_activities(user_id)
        withdraws = [activity for activity in activities if activity.activity_type == ActivityType.WITHDRAW.value]
        if len(withdraws) >= 3:
            last_three = withdraws[-3:]
            if all(last_three[i].timestamp < last_three[i+1].timestamp for i in range(2)):
                return True
        return False

    def check_increasing_deposits(self, user_id):
        activities = self.activity_repository.get_user_activities(user_id)
        deposits = [activity for activity in activities if activity.activity_type == ActivityType.DEPOSIT.value]
        if len(deposits) >= 3:
            last_three = deposits[-3:]
            if all(last_three[i].amount < last_three[i+1].amount for i in range(2)):
                return True
        return False

    def check_accumulative_deposit(self, user_id):
        current_time = self.activity_repository.get_latest_timestamp(user_id)
        thirty_seconds_ago = current_time - timedelta(seconds=30)
        
        recent_deposits = self.activity_repository.get_recent_deposits(user_id, thirty_seconds_ago)
        total_amount = sum(deposit.amount for deposit in recent_deposits)
        return total_amount > 200

