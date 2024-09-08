from rest_framework import routers
from rest_framework.authtoken import views
from django.urls import path, include

from .views import CommentViewSet, GroupViewSet, PostViewSet, FollowViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('posts/(?P<post_id>[^/.]+)/comments',
                CommentViewSet, basename='comment')
router.register('groups', GroupViewSet)
router.register('posts', PostViewSet)
router.register('follow', FollowViewSet)
router_comment = routers.DefaultRouter()

urlpatterns = [
    path('', include('djoser.urls.jwt')),
    path('', include(router.urls)),
]
