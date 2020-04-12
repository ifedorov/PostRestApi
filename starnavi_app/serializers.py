from django.contrib.auth import authenticate
from django.core import exceptions
from django.utils.translation import gettext as _
from rest_framework import serializers

from starnavi_app.models import Post, User, Like


class AuthCustomTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email_or_username = attrs.get('email')
        password = attrs.get('password')

        if email_or_username and password:
            user = authenticate(email=email_or_username, password=password)
            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise exceptions.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Must include "email" and "password"')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'content', 'date_dump')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class LikeSerializer(serializers.ModelSerializer):
    is_like = serializers.BooleanField(read_only=True)
    post = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'is_like', 'post', 'user')

    def create(self, validated_data):
        instance, _ = Like.objects.update_or_create(
            **validated_data, defaults={'is_like': True}
        )
        return instance


class UnlikeSerializer(serializers.ModelSerializer):
    is_like = serializers.BooleanField(read_only=True)
    post = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'is_like', 'post', 'user')

    def create(self, validated_data):
        instance, _ = Like.objects.update_or_create(
            **validated_data, defaults={'is_like': False}
        )
        return instance
