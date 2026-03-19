import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from ..models import Video, VideoLike
from ..serializers import VideoSerializer


@pytest.mark.django_db
class TestVideoSerializer:
  def test_valid_data_serializes_correctly(self, mock_video):
    serializer = VideoSerializer(mock_video)
    data = serializer.data

    assert data["title"] == "Mock Video from Tests"
    assert data["description"] == "This is a video made as a mock from the test"
    assert "id" in data

  def test_contains_expected_fields(self, mock_video):
    serializer = VideoSerializer(mock_video)
    fields = set(serializer.data.keys())

    assert fields == {"id", "title", "description", "user", "created_at", "updated_at", "likes", "dislikes", "views", "video_url", "thumbnail_url", "file_id"}