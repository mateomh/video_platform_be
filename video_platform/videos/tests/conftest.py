# users/tests/conftest.py
import pytest
from django.contrib.auth.models import User
from ..models import Video

@pytest.fixture
def video_user():
    return User.objects.create(
        username="johndoe",
        email="john@example.com"
    )


@pytest.fixture
def mock_video(video_user):
    return Video.objects.create(
      user = video_user,
      title = 'Mock Video from Tests',
      description = 'This is a video made as a mock from the test'
    )