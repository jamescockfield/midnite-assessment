import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from services.alert_builder import AlertBuilder
from domain_types import ActivityType, AlertCode
from database.models import UserActivity

@pytest.fixture
def mock_repository():
    repository = Mock()
    repository.get_user_activities.return_value = []
    repository.get_latest_timestamp.return_value = datetime.now()
    repository.get_recent_deposits.return_value = []
    return repository

@pytest.fixture
def alert_builder(mock_repository):
    return AlertBuilder(mock_repository)

def test_large_withdrawal_alert(alert_builder, mock_repository):
    # Arrange
    activity = UserActivity(
        user_id=1,
        activity_type=ActivityType.WITHDRAW.value,
        amount=150,
        timestamp=datetime.now()
    )
    
    # Act
    alerts = alert_builder.build_alerts(activity)
    
    # Assert
    assert AlertCode.LARGE_WITHDRAWAL.value in alerts

def test_no_large_withdrawal_alert_for_small_amount(alert_builder, mock_repository):
    # Arrange
    activity = UserActivity(
        user_id=1,
        activity_type=ActivityType.WITHDRAW.value,
        amount=50,
        timestamp=datetime.now()
    )
    
    # Act
    alerts = alert_builder.build_alerts(activity)
    
    # Assert
    assert AlertCode.LARGE_WITHDRAWAL.value not in alerts

def test_consecutive_withdrawals_alert(alert_builder, mock_repository):
    # Arrange
    now = datetime.now()
    activities = [
        UserActivity(user_id=1, activity_type=ActivityType.WITHDRAW.value, amount=50, timestamp=now - timedelta(minutes=2)),
        UserActivity(user_id=1, activity_type=ActivityType.WITHDRAW.value, amount=75, timestamp=now - timedelta(minutes=1)),
        UserActivity(user_id=1, activity_type=ActivityType.WITHDRAW.value, amount=100, timestamp=now)
    ]
    mock_repository.get_user_activities.return_value = activities
    mock_repository.get_latest_timestamp.return_value = now
    
    activity = UserActivity(
        user_id=1,
        activity_type=ActivityType.WITHDRAW.value,
        amount=150,
        timestamp=now
    )
    
    # Act
    alerts = alert_builder.build_alerts(activity)
    
    # Assert
    assert AlertCode.CONSECUTIVE_WITHDRAWALS.value in alerts

def test_increasing_deposits_alert(alert_builder, mock_repository):
    # Arrange
    now = datetime.now()
    activities = [
        UserActivity(user_id=1, activity_type=ActivityType.DEPOSIT.value, amount=50, timestamp=now - timedelta(minutes=2)),
        UserActivity(user_id=1, activity_type=ActivityType.DEPOSIT.value, amount=75, timestamp=now - timedelta(minutes=1)),
        UserActivity(user_id=1, activity_type=ActivityType.DEPOSIT.value, amount=100, timestamp=now)
    ]
    mock_repository.get_user_activities.return_value = activities
    mock_repository.get_latest_timestamp.return_value = now
    
    activity = UserActivity(
        user_id=1,
        activity_type=ActivityType.DEPOSIT.value,
        amount=150,
        timestamp=now
    )
    
    # Act
    alerts = alert_builder.build_alerts(activity)
    
    # Assert
    assert AlertCode.INCREASING_DEPOSITS.value in alerts

def test_accumulative_deposit_alert(alert_builder, mock_repository):
    # Arrange
    now = datetime.now()
    mock_repository.get_latest_timestamp.return_value = now
    recent_deposits = [
        UserActivity(user_id=1, activity_type=ActivityType.DEPOSIT.value, amount=100, timestamp=now - timedelta(seconds=20)),
        UserActivity(user_id=1, activity_type=ActivityType.DEPOSIT.value, amount=150, timestamp=now - timedelta(seconds=10))
    ]
    mock_repository.get_recent_deposits.return_value = recent_deposits
    
    activity = UserActivity(
        user_id=1,
        activity_type=ActivityType.DEPOSIT.value,
        amount=100,
        timestamp=now
    )
    
    # Act
    alerts = alert_builder.build_alerts(activity)
    
    # Assert
    assert AlertCode.ACCUMULATIVE_DEPOSIT.value in alerts

def test_no_alerts_for_normal_activity(alert_builder, mock_repository):
    # Arrange
    activity = UserActivity(
        user_id=1,
        activity_type=ActivityType.DEPOSIT.value,
        amount=50,
        timestamp=datetime.now()
    )
    
    # Act
    alerts = alert_builder.build_alerts(activity)
    
    # Assert
    assert len(alerts) == 0
