from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse

from .models import Video, Comments


class VideosListView(ListView):
    model = Video
    template_name = 'services/home.html'
    context_object_name = 'videos'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(description__icontains=query)

        for video in queryset:
            video.count_views += 1
            video.save()
        return queryset


class VideoCreateView(LoginRequiredMixin, CreateView):
    model = Video
    fields = ['description', 'video_file']
    template_name = 'services/video_create.html'
    success_url = reverse_lazy('video_view')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


@login_required
def like_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.user in video.likes.all():
        video.likes.remove(request.user)
        liked = False
    else:
        video.likes.add(request.user)
        liked = True
    return JsonResponse({
        'liked': liked,
        'likes_count': video.likes.count()
    })


@login_required
def add_comment(request, video_id):
    if request.method == 'POST':
        video = get_object_or_404(Video, id=video_id)
        text = request.POST.get('text')
        if text:
            comment = Comments.objects.create(user=request.user, text=text)
            video.comments.add(comment)
        return redirect('video_view')


class VideoEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Video
    fields = ['description', 'video_file']
    template_name = 'services/video_edit.html'
    success_url = reverse_lazy('video_view')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        print(f"Editing video: {obj.id}")
        return obj

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def test_func(self):
        video = self.get_object()
        return self.request.user == video.creator


class VideoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Video
    template_name = 'services/video_delete.html'
    success_url = reverse_lazy('video_view')

    def test_func(self):
        video = self.get_object()
        return self.request.user == video.creator
