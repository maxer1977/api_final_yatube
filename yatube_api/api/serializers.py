from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


from posts.models import Comment, Post, Follow, Group, User


class PostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Post.
    В поле автор подменяется значение ключа-индекса на username.
    """
    author = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field='username')

    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group')
        read_only_fields = ('author', 'pub_date')


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group."""
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')
        read_only_fields = ('title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Comments.
    В поле автор подменяется значение ключа-индекса на username.
    """
    author = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'post', 'created')
        read_only_fields = ('author', 'post')


class FollowSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Follow.
    Для записи/вывода полей user (подписчик) и following (автор)
    подставляются значения поля username, но сохраняется id.
    """
    user = serializers.SlugRelatedField(
        many=False, read_only=False, slug_field='username',
        queryset=User.objects.all(), default=serializers.CurrentUserDefault())
    following = serializers.SlugRelatedField(
        many=False, read_only=False, slug_field='username',
        queryset=User.objects.all())

    class Meta:
        """
        К стандартным настройкам добавлен контроль - validator.
        Пользователь может создать только одну подписку на каждого автора.
        """
        model = Follow
        fields = ('id', 'user', 'following',)
        read_only_fields = ('id', 'user',)
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'])
        ]

    def validate(self, data):
        """
        Исключение возможности создания автором подписки у самого себя.
        """
        if data['following'] == data['user']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!')
        return data
