from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404
from . import forms
from . import models
from django.contrib.auth import get_user_model

User = get_user_model()

class PostList(generic.ListView):
    model = models.Post
    template_name = "posts/post_list.html"  

class UserPosts(generic.ListView):
    model = models.Post
    template_name = "posts/user_post_list.html"

    def get_queryset(self):
        self.post_user = get_object_or_404(User, username__iexact=self.kwargs.get("username"))
        return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context

class PostDetail(generic.DetailView):
    model = models.Post
    template_name = "posts/post_detail.html" 

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get("username"))

class CreatePost(LoginRequiredMixin, generic.CreateView):
    model = models.Post
    template_name = "posts/post_form.html"  
    fields = ('message','group')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class DeletePost(LoginRequiredMixin, generic.DeleteView):
    model = models.Post
    template_name = "posts/post_confirm_delete.html"  
    success_url = reverse_lazy("posts:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)
