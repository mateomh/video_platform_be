# users/tests/conftest.py
import pytest
from django.contrib.auth.models import User

@pytest.fixture
def video_user():
    return User.objects.create(
        username="johndoe",
        email="john@example.com"
    )