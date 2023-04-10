from rest_framework import serializers
from assignment_app.models import PostModel


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = "__all__"