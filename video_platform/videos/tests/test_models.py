import pytest
from django.contrib.auth.models import User
from ..models import Video, VideoLike

@pytest.mark.django_db
class TestVideoModel:
  def test_video_model(self):
    user = User.objects.create(
      username="johndoe",
      email="john@example.com"
    )

    video = Video.objects.create(
      user = user,
      title = 'Test Video from Tests',
      description = 'This is a video made from the test'
    )

    assert video.id is not None # type: ignore
    assert video.title == 'Test Video from Tests'
    assert video.description == 'This is a video made from the test'
    assert video.likes == 0
    assert video.dislikes == 0
    assert video.views == 0


@pytest.mark.django_db
class TestVideoLikeModel:
  def test_video_like_model(self):
    user = User.objects.create(
      username="johndoe",
      email="john@example.com"
    )

    video = Video.objects.create(
      user = user,
      title = 'Test Video from Tests',
      description = 'This is a video made from the test'
    )

    like = VideoLike.objects.create(
      user = user,
      video = video,
      value = VideoLike.LIKE
    )

    assert like.id is not None # type: ignore
    assert like.value == 1

