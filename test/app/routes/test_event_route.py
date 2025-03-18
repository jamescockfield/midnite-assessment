import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from flask import Flask
from flask_injector import FlaskInjector
from app.routes.event_route import event_bp, handle_event
from app.requests.event_request import EventRequest
from domain_types import ActivityType
from database.models import UserActivity
from services import AlertBuilder
from repositories.user_activity_repository import UserActivityRepository
from pydantic import ValidationError

@pytest.fixture
def mock_activity_repository():
    return Mock()

@pytest.fixture
def mock_alert_builder():
    return Mock()

@pytest.fixture
def app(mock_activity_repository, mock_alert_builder):
    app = Flask(__name__)
    app.register_blueprint(event_bp)
    
    def configure(binder):
        binder.bind(UserActivityRepository, to=mock_activity_repository)
        binder.bind(AlertBuilder, to=mock_alert_builder)
    
    FlaskInjector(app=app, modules=[configure])
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_successful_deposit_event(client, mock_activity_repository, mock_alert_builder):
    # Arrange
    event_data = {
        "type": ActivityType.DEPOSIT.value,
        "amount": "100.50",
        "user_id": 123,
        "t": int(datetime.now().timestamp())
    }
    mock_alert_builder.build_alerts.return_value = []
    
    # Act
    response = client.post('/event', json=event_data)
    
    # Assert
    assert response.status_code == 200
    assert response.json == {
        "alert": False,
        "alert_codes": [],
        "user_id": "123"
    }
    mock_activity_repository.add_activity.assert_called_once()
    mock_alert_builder.build_alerts.assert_called_once()

def test_successful_withdraw_event_with_alert(client, mock_alert_builder):
    # Arrange
    event_data = {
        "type": ActivityType.WITHDRAW.value,
        "amount": "1000.00",
        "user_id": 123,
        "t": int(datetime.now().timestamp())
    }
    mock_alert_builder.build_alerts.return_value = ["LARGE_WITHDRAWAL"]
    
    # Act
    response = client.post('/event', json=event_data)
    
    # Assert
    assert response.status_code == 200
    assert response.json == {
        "alert": True,
        "alert_codes": ["LARGE_WITHDRAWAL"],
        "user_id": "123"
    }

def test_invalid_activity_type(app, mock_activity_repository, mock_alert_builder):
    # Arrange
    event_data = {
        "type": "invalid_type",
        "amount": "100.50",
        "user_id": 123,
        "t": int(datetime.now().timestamp())
    }
    
    # Act & Assert
    with app.test_request_context('/event', json=event_data, method='POST'):
        with pytest.raises(ValidationError):
            handle_event(mock_activity_repository, mock_alert_builder)

def test_invalid_amount(app, mock_activity_repository, mock_alert_builder):
    # Arrange
    event_data = {
        "type": ActivityType.DEPOSIT.value,
        "amount": "invalid_amount",
        "user_id": 123,
        "t": int(datetime.now().timestamp())
    }
    
    # Act & Assert
    with app.test_request_context('/event', json=event_data, method='POST'):
        with pytest.raises(ValidationError):
            handle_event(mock_activity_repository, mock_alert_builder)

def test_missing_json_data(app, mock_activity_repository, mock_alert_builder):
    with app.test_request_context('/event', json='', method='POST'):
        with pytest.raises(ValueError):
            handle_event(mock_activity_repository, mock_alert_builder)

def test_missing_required_fields(app, mock_activity_repository, mock_alert_builder):
    # Arrange
    event_data = {
        "type": ActivityType.DEPOSIT.value,
        "amount": "100.50"
        # Missing user_id and t
    }
    
    # Act & Assert
    with app.test_request_context('/event', json=event_data, method='POST'):
        with pytest.raises(ValidationError):
            handle_event(mock_activity_repository, mock_alert_builder)
