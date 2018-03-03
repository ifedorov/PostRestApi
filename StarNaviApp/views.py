# Create your views here.
from rest_framework import permissions, status, mixins
from rest_framework.authtoken.models import Token
from rest_framework.decorators import detail_route
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from StarNaviApp.models import Post
from StarNaviApp.serializers import PostSerializer, UserSerializer, AuthCustomTokenSerializer, LikeSerializer, \
    UnlikeSerializer


class IsAuthOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated


class PostViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthOrReadOnly,)
    http_method_names = ['get', 'post', 'put', 'head', 'option']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def like(self, request, pk):

        post = get_object_or_404(Post, pk=pk)

        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def unlike(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        serializer = UnlikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreateViewSet(mixins.CreateModelMixin,
                        GenericViewSet):
    permission_classes = (AllowAny,)
    http_method_names = ['post']


    def token(self, request):
        serializer = AuthCustomTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        content = {
            'token': token.key,
        }
        return Response(content)

    def sing_up(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('User created successfully', status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


