from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)
from django.shortcuts import get_object_or_404
from posts.models import Group, Post
from rest_framework import filters, mixins, permissions, viewsets

from .permissions import AuthorOrReadOnly, ReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    """Управление функциями для работы с комментариями."""

    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_permissions(self):
        """
        Переопределение прав доступа к комментариями.
        Просмотр для любой категории пользователей.
        Полный доступ для автора комментария.
        """
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def get_queryset(self):
        """
        Переопределение queryset.
        Отбор комментариев относящихся к определенному посту.
        """
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        new_queryset = post.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        """
        Переопределение create().
        Подстановка автора и поста к новому комментарию.
        """
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post=post)


class PostViewSet(viewsets.ModelViewSet):
    """Управление функциями для работы с постами."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_permissions(self):
        """
        Переопределение прав доступа для просмотра поста.
        Доступно любой категории пользователя.
        """
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Переопределение create().
        Подстановка автора к новому посту.
        """
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Управление функциями для работы с группами постов.
    Доступно только чтение любой категории пользователей.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.AllowAny,)


class CreateListViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """
    Базовый класс с возможностью !только! создания записей и получения списка.
    """

    pass


class FollowViewSet(CreateListViewSet):
    """
    Управление функциями для работы с подписками.
    Только создание записи и солучение списка подписок.
    """

    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """
        Переопределение queryset.
        Отбор подписок, созданных пользователем-инициатором запроса.
        """
        user = self.request.user
        new_queryset = user.follower.all()
        return new_queryset

    def get_permissions(self):
        """
        Переопределение прав доступа к подпискам.
        Только для аутентифицированного пользователя доступно:
        - просмотр списка своих подписок
        - создание новой подписки
        """
        if self.action == 'create':
            return (AuthorOrReadOnly(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Переопределение create().
        Подстановка пользователя к новой подписке.
        """
        serializer.save(user=self.request.user)
