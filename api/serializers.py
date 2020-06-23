from rest_framework import serializers
from users.models import User
from core.models import Question, Answer

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'is_staff']

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Question
        fields = ['url', 'title', 'body', 'user']

