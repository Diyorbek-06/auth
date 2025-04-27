from rest_framework import serializers
from product.models.products import Post


class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'