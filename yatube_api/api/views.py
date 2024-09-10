from rest_framework import viewsets, exceptions, mixins, permissions, filters
from rest_framework.pagination import LimitOffsetPagination
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404

from .mixins import CommentPostBaseMixin
from .permissions import OwnerOrReadOnly
from .serializers import (PostSerializer, GroupSerializer,
                          CommentSerializer, FollowSerializer)
from posts.models import Group, Post, Follow, User


class CommentViewSet(CommentPostBaseMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    object_viewset = 'комментарии'
    permission_classes = (OwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())

    def get_post(self):
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, id=post_id)

    def get_queryset(self):
        return self.get_post().comments.all()


class FollowViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username', )

    def get_queryset(self):
        user = self.request.user
        return User.objects.get(username=user).follower.all()

    # def perform_create(self, serializer):
    #     following = serializer.validated_data.get('following')
    #     try:
    #         serializer.save(user=self.request.user)
    #     except IntegrityError:
    #         raise exceptions.ParseError(f'Вы уже подписаны на {following}')


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.AllowAny,)


class PostViewSet(CommentPostBaseMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    object_viewset = 'посты'
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
