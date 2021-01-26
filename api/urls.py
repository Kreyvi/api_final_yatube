from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

v1_router = DefaultRouter()
v1_router.register(
    'posts',
    PostViewSet,
    basename='posts'
)
v1_router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

v1_router.register(
    'group',
    GroupViewSet,
    basename='group'
)

v1_router.register(
    'follow',
    FollowViewSet,
    basename='follow'
)


urlpatterns = [
    path('', include(v1_router.urls)),
]
