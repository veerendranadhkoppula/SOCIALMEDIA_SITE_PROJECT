from django.urls import path,re_path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostList.as_view(), name='all'),
    path('new/', views.CreatePost.as_view(), name='create'),
    re_path(r'^by/(?P<username>[-\w]+)', views.UserPosts.as_view(), name='for_user'),
    re_path(r'^by/(?P<username>[-\w]+)/(?P<pk>\d+)/$', views.PostDetail.as_view(), name='single'),
    re_path(r'^delete/(?P<pk>\d+)/$', views.DeletePost.as_view(), name='delete'),
]