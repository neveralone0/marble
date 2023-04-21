from django.shortcuts import render
from django.utils.baseconv import base64
from rest_framework import viewsets, permissions
from rest_framework.views import APIView, Response, status
from .models import *
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.base import ContentFile


class PostResponceAPI(APIView):
    serializer_class = PostResponceSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        posts = Posts.objects.all()
        srz_data = self.serializer_class(instance=posts, many=True, context={'request': request})
        return Response(srz_data.data)


class PostAPI(APIView):
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        posts = Posts.objects.all()
        srz_data = self.serializer_class(instance=posts, many=True)
        return Response(srz_data.data)

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid():
            user = User.objects.get(id=request.user.id)
            srz_data.validated_data['owner'] = user
            print(srz_data.validated_data['owner'])
            srz_data.create(validated_data=srz_data.validated_data)
            return Response({'msg': 'post uploaded'}, status=status.HTTP_201_CREATED)
        print(srz_data.errors)
        return Response(srz_data.errors)
        # data = request.POST.get('img')
        # image_data = ContentFile(base64.b64decode(data), name='image.jpg')
        # post = Posts.objects.create()
        # post.caption = request.data['caption']
        # post.img = image_data
        # post.save()
        # return Response({'status': 'ok'})


class MyModelViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.order_by('-caption')
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostLike(APIView):
    def get(self, request, id):
        post = Posts.objects.get(id=id)
        like = Likes.objects.filter(post=post, user=request.user.id)
        if like:
            like.delete()
            return Response({'msg': 'disliked'})
        Likes.objects.create(post=post, user=request.user)
        return Response({'msg': 'liked'})
