from rest_framework import viewsets, exceptions, mixins, permissions, filters
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404

from .serializers import (PostSerializer, GroupSerializer,
                          CommentSerializer, FollowSerializer)
from .permissions import OwnerOrReadOnly
from posts.models import Group, Post, Follow


class CommentPostBaseMixin(mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin):

    def perform_create(self, serializer):
        if self.serializer_class == CommentSerializer:
            serializer.save(author=self.request.user, post=self.get_post())
        else:
            serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise exceptions.PermissionDenied(
                f"Вы не можете редактировать чужие {self.object_viewset}!")
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise exceptions.PermissionDenied(
                f"Вы не можете удалять чужие {self.object_viewset}!")
        super().perform_destroy(instance)


class CommentViewSet(CommentPostBaseMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    object_viewset = 'комментарии'
    permission_classes = (OwnerOrReadOnly,)

    def get_post(self):
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, id=post_id)

    def get_queryset(self):
        return self.get_post().comments


class FollowViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username', )

    def get_queryset(self):
        queryset = Follow.objects.all()
        user = self.request.user
        queryset = queryset.filter(user=user)
        return queryset

    def perform_create(self, serializer):
        if serializer.validated_data.get('following') == self.request.user:
            raise exceptions.ParseError('Нельзя подписаться на самого себя')
        try:
            serializer.save(user=self.request.user)
        except:
            following = serializer.data['following']
            raise exceptions.ParseError(f'Вы уже подписаны на {following}')


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
