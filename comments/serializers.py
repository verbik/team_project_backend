from rest_framework import serializers

from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "content_type", "object_id", "created_at", "comment_contents")
        read_only_fields = ("created_at", "content_type", "object_id")
