from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, viewsets

from posts.models import Comment, Group, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    # ModelViewSet сразу даёт все CRUD-операции
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        # подставляем автора из запроса, а не из данных
        serializer.save(author=self.request.user)


class GroupViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    # только чтение — POST/PUT/DELETE вернут 405
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated,)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated, IsAuthorOrReadOnly)

    def get_post(self):
        # достаём пост из URL-параметра, 404 если не существует
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        # возвращаем только комментарии конкретного поста
        return Comment.objects.filter(post=self.get_post())

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())