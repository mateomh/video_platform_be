from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from rest_framework import authentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Video, VideoLike
from .forms import VideoUploadForm
from .imagekit_client import upload_video, upload_thumbnail, delete_video
from videos.serializers import VideoSerializer


@api_view(['GET'])
def video_detail(request, video_id):
    video = get_object_or_404(Video.objects, id=video_id)

    video.views += 1
    video.save(update_fields=["views"])

    user_vote = None
    if request.user.is_authenticated:
        like = VideoLike.objects.filter(user=request.user, video=video).first()
        if like:
            user_vote = like.value

    serialized_video = VideoSerializer(video)
    return Response(serialized_video.data)

@api_view(['GET'])
def video_list(request):
    videos = Video.objects.all()
    serialized_videos = VideoSerializer(videos, many=True)
    return Response(serialized_videos.data)    

@api_view(['GET'])
def channel_videos(request, username):
    videos = Video.objects.filter(user__username=username)
    serialized_videos = VideoSerializer(videos, many=True)

    return Response(serialized_videos.data) 


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([IsAuthenticated])
def video_upload(request):
  form = VideoUploadForm(request.POST, request.FILES)
  print(f"FORM VALID: {form.is_valid()}")
  print(f"REQUEST DATA: {request.user}")

  if form.is_valid():
    video_file = form.cleaned_data['video_file']
    custom_thumbnail = form.cleaned_data['thumbnail_file']

    try:
      result = upload_video(
        file_data=video_file.read(),
        file_name=video_file.name
      )

      print(f"VIDEO UPLOAD RESULT: {result}")

      thumbnail_url = ''
      if custom_thumbnail:
        try:
          base_name = video_file.name.rsplit('.', 1)[0]
          thumb_result = upload_thumbnail(
            file_data=custom_thumbnail,
            file_name=base_name + '_thumb.jpg'
          )

          thumbnail_url = thumb_result['url']
        except Exception as e:
          pass

      video = Video.objects.create(
        user=request.user,
        title=form.cleaned_data['title'],
        description=form.cleaned_data['description'],
        file_id=result['file_id'],
        video_url=result['url'],
        thumbnail_url=thumbnail_url,
      )

      return JsonResponse({
        "success": True,
        "video_id": video.id,
        "message": "Video uploaded successfully"
      })
    except Exception as e:
      print("this is the ERRORRRRRRRRRRRRRRRR")
      print(e)
      return JsonResponse({
        "success": False,
        "error": str(e)
      })
  
  errors = []
  for field, field_errors in form.errors.items():
    for error in field_errors:
      print("this is the ERRORRRRRRRRRRRRRRRR")
      print(error)
      errors.append(f"{field}: {error}" if field != '__all__' else error)

  return JsonResponse({
    "success": False,
    "error": ';'.join(errors)
  })


@api_view(['DELETE'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_video(request, video_id):
  video = get_object_or_404(Video, id=video_id, user=request.user)
  
  try:
    delete_video(video.file_id)
  except Exception as e:
    print(e)
    pass

  video.delete()

  return JsonResponse({
    "success": True,
    "message": "Video deleted"
  })


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([IsAuthenticated])
def video_vote(request, video_id):
  video = get_object_or_404(Video, id=video_id, user=request.user)
  vote_type = request.data['vote']

  if vote_type not in ['like', 'dislike']:
     return JsonResponse({
        "success": False,
        "error": "Invalid vote",
        "status": 400
     })
  
  value = VideoLike.LIKE if vote_type == 'like' else VideoLike.DISLIKE

  existing_vote = VideoLike.objects.filter(user=request.user, video=video).first()

  if existing_vote:
    if existing_vote.value == value:
        if value == VideoLike.LIKE:
            video.likes -= 1
        else:
            video.dislikes -= 1
        existing_vote.delete()
        user_vote = None
    else:
        if value == VideoLike.LIKE:
            video.likes += 1
            video.dislikes -= 1
        else:
            video.likes -=1
            video.dislikes += 1
        existing_vote.value = value
        existing_vote.save()
        user_vote = value
  else:
      VideoLike.objects.create(user=request.user, video=video, value=value)
      if value == VideoLike.LIKE:
          video.likes += 1
      else:
          video.dislikes += 1
      user_vote = value

  video.save(update_fields=["likes", "dislikes"])

  return JsonResponse({
    "likes": video.likes,
    "dislikes": video.dislikes,
    "user_vote": user_vote
  })


