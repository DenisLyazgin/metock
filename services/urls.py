from django.urls import path
from .views import VideosListView, like_video, add_comment, VideoEditView, VideoDeleteView, VideoCreateView

urlpatterns = [
    path('', VideosListView.as_view(), name='video_view'),
    path('like/<int:video_id>/', like_video, name='like_video'),
    path('comment/<int:video_id>/', add_comment, name='add_comment'),
    path('video/<int:pk>/edit/', VideoEditView.as_view(), name='video_edit'),
    path('video/<int:pk>/delete/', VideoDeleteView.as_view(), name='video_delete'),
    path('video/create/', VideoCreateView.as_view(), name='video_create'),
]
