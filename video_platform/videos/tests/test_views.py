import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from unittest.mock import patch
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


@pytest.mark.django_db
class TestVideoDetailView:
  def test_video_detail_return_200(self, client, mock_video):
    url = reverse('videos:detail', kwargs = { "video_id": mock_video.id})
    response = client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert data['id'] == mock_video.id
    assert data['title'] == mock_video.title
    assert data['description'] == mock_video.description
    assert data['likes'] == mock_video.likes
    assert data['dislikes'] == mock_video.likes


@pytest.mark.django_db
class TestVideoUploadView:
  def test_unauthenticated_user_is_rejected(self, client, video_file):
    url = reverse('videos:upload_video')
    response = client.post(url, {
        "title": "Test",
        "description": "Test",
        "video_file": video_file
    })
    
    assert response.status_code == 401  # or 403


  def test_missing_title_returns_error(self, authenticated_client, video_user, video_file):
    url = reverse('videos:upload_video')
    response = authenticated_client.post(url, {
        "description": "No title here",
        "video_file": video_file
    })
    data = response.json()

    assert data["success"] is False
    assert "title" in data["error"]


  def test_missing_video_file_returns_error(self, authenticated_client, video_user):
    url = reverse('videos:upload_video')
    response = authenticated_client.post(url, {
        "title": "No file",
        "description": "Missing file"
    })
    data = response.json()

    assert data["success"] is False
    assert "video_file" in data["error"]


  @patch("videos.views.upload_video")
  def test_successful_upload_returns_200(
    self, mock_upload_video, authenticated_client, video_file
  ):
    mock_upload_video.return_value = {
        "file_id": "abc123",
        "url": "https://cdn.example.com/video.mp4"
    }
    url = reverse('videos:upload_video')

    response = authenticated_client.post(url, {
        "title": "My Video",
        "description": "A test video",
        "video_file": video_file
    }, format="multipart")
    data = response.json()

    assert response.status_code == 200
    assert data["success"] is True
    assert "video_id" in data
    assert data["message"] == "Video uploaded successfully"


  @patch("videos.views.upload_video")
  def test_successful_upload_creates_video_in_db(
    self, mock_upload_video, authenticated_client, video_user, video_file
  ):
    mock_upload_video.return_value = {
        "file_id": "abc123",
        "url": "https://cdn.example.com/video.mp4"
    }
    url = reverse('videos:upload_video')

    authenticated_client.post(url, {
        "title": "My Video",
        "description": "A test video",
        "video_file": video_file
    })

    assert Video.objects.count() == 1
    video = Video.objects.first()
    assert video.title == "My Video" # type: ignore
    assert video.user == video_user # type: ignore
    assert video.file_id == "abc123" # type: ignore


  @patch("videos.views.upload_thumbnail")
  @patch("videos.views.upload_video")
  def test_custom_thumbnail_is_uploaded(
      self, mock_upload_video, mock_upload_thumbnail, authenticated_client, video_file, thumbnail_file
  ):
    mock_upload_video.return_value = {
        "file_id": "abc123",
        "url": "https://cdn.example.com/video.mp4"
    }
    mock_upload_thumbnail.return_value = {
        "url": "https://cdn.example.com/thumb.jpg"
    }
    url = reverse('videos:upload_video')

    response = authenticated_client.post(url, {
        "title": "My Video",
        "description": "A test video",
        "video_file": video_file,
        "thumbnail_file": thumbnail_file
    })
    data = response.json()

    assert data["success"] is True
    mock_upload_thumbnail.assert_called_once()
    assert Video.objects.first().thumbnail_url == "https://cdn.example.com/thumb.jpg" # type: ignore


  @patch("videos.views.upload_thumbnail")
  @patch("videos.views.upload_video")
  def test_failed_thumbnail_upload_still_creates_video(
      self, mock_upload_video, mock_upload_thumbnail, authenticated_client, video_file, thumbnail_file
  ):
    mock_upload_video.return_value = {
        "file_id": "abc123",
        "url": "https://cdn.example.com/video.mp4"
    }
    mock_upload_thumbnail.side_effect = Exception("Thumbnail service down")
    url = reverse('videos:upload_video')

    response = authenticated_client.post(url, {
        "title": "My Video",
        "description": "A test video",
        "video_file": video_file,
        "thumbnail_file": thumbnail_file
    })
    data = response.json()

    # video still created even if thumbnail fails
    assert data["success"] is True
    assert Video.objects.first().thumbnail_url == "" # type: ignore
