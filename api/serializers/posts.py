from rest_framework import serializers 

from api.models import Media, Post, Comment
from .users import UserSerializer 

class PostSerializer(serializers.ModelSerializer):
	user = UserSerializer()

	class Meta:
		model  = Post
		fields = "__all__"
class MediaSerializer(serializers.ModelSerializer): 
	class Meta: 
		model = Media 
		fields = "__all__"


class CommentSerializer(serializers.Serializer):
    class Meta:
        model = Comment
        fields = '__all__'