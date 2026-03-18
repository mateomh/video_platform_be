import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from ..models import Video, VideoLike


@pytest.mark.django_db
class TestVideoListView:
  def test_video_list_return_200(self, client):
    url = reverse('videos:list')
    response = client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert data == []

  def test_video_list_return_available_videos(self, client, mock_video):
    url = reverse('videos:list')
    response = client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert data != []

  