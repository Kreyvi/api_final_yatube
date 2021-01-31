from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin, ListModelMixin, \
    RetrieveModelMixin
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.viewsets import GenericViewSet

from api.models import Group, Post
from api.permissions import IsAuthorOrReadOnly
from . import serializers


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


class GroupViewSet(viewsets.GenericViewSet, CreateModelMixin, ListModelMixin):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer


class FollowViewSet(viewsets.GenericViewSet, CreateModelMixin, ListModelMixin):
    serializer_class = serializers.FollowSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username']

    def get_queryset(self):
        user = self.request.user
        queryset = user.following
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
