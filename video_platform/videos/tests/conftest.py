# users/tests/conftest.py
import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from ..models import Video

@pytest.fixture
def video_user():
    return User.objects.create(
        username="johndoe",
        email="john@example.com"
    )

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_client(video_user):
    client = APIClient()
    token, _ = Token.objects.get_or_create(user=video_user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return client

@pytest.fixture
def mock_video(video_user):
    return Video.objects.create(
      user = video_user,
      title = 'Mock Video from Tests',
      description = 'This is a video made as a mock from the test'
    )

@pytest.fixture
def video_file():
    return SimpleUploadedFile(
        name="test_video.mp4",
        content=b"fake video content",
        content_type="video/mp4"
    )

@pytest.fixture
def thumbnail_file():
    return SimpleUploadedFile(
        name="test_thumb.jpg",
        content=b"fake image content",
        content_type="image/jpeg"
    )
