from flask import Blueprint, request, jsonify
from datetime import datetime
from services import AlertBuilder
from repositories.user_activity_repository import UserActivityRepository
from database.database import db
from flask_injector import inject
from database.models import UserActivity
from app.requests import EventRequest

event_bp = Blueprint('event', __name__)

@event_bp.route('/event', methods=['POST'])
@inject
def handle_event(activity_repository: UserActivityRepository, alert_builder: AlertBuilder):
    data = request.get_json()
    if not data:
        raise ValueError("No JSON data provided")

    validated_data = EventRequest(**data)
    
    activity = UserActivity(
        user_id=str(validated_data.user_id),
        activity_type=validated_data.type,
        amount=float(validated_data.amount),
        timestamp=datetime.fromtimestamp(validated_data.t)
    )
    
    activity_repository.add_activity(activity)

    alert_codes = alert_builder.build_alerts(activity)

    response = {
        "alert": len(alert_codes) > 0,
        "alert_codes": alert_codes,
        "user_id": activity.user_id
    }

    return jsonify(response)
