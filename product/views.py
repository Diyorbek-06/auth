from .serializers import PostSerializers
from product.models.products import Post
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
# Create your views here.

class Posts(generics.GenericAPIView):
     permission_classes = [permissions.IsAuthenticated]
     authentication_classes = [TokenAuthentication]

     def get(self, request, *args, **kwargs):
          posts = Post.objects.all()
          serializer = PostSerializers(posts, many=True)
          return Response({
               'data': serializer.data,

          })

class CreateProduct(generics.CreateAPIView):
     serializer_class = PostSerializers
     queryset = Posts