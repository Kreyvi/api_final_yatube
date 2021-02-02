from rest_framework import filters, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly
)

from api.models import Group, Post
from api.permissions import IsAuthorOrReadOnly
from . import serializers
from .viewsets import ListCreateViewSet


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    filterset_fields = ['group', ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        return post.comments

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        serializer.save(
            author=self.request.user,
            post=post,
        )


class GroupViewSet(ListCreateViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer


class FollowViewSet(ListCreateViewSet):
    serializer_class = serializers.FollowSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username']

    def get_queryset(self):
        user = self.request.user
        queryset = user.following
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
