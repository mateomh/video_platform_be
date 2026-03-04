from django import forms


class VideoUploadForm(forms.Form):

    title = forms.CharField(
        max_length=200,
    )
    description = forms.CharField(
        required=False,
    )
    video_file = forms.FileField()
    thumbnail_file = forms.FileField(
        required=False,
    )

    def clean_video_file(self):
        video = self.cleaned_data.get("video_file")
        if video:
            if video.size > 100 * 1024 * 1024:
                raise forms.ValidationError("Video must be under 100mb")

            allowed_types = ["video/mp4", "video/webm", "video/quicktime", "video/x-msvideo"]
            if video.content_type not in allowed_types:
                raise forms.ValidationError("This video type is not allowed.")

        return video