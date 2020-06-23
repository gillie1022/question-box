from rest_framework import serializers
from users.models import User
from core.models import Question, Answer

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'is_staff',]

class AnswerSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    class Meta:
        model = Answer
        fields = ['author', 'body', 'answered_on', "marked_correct",]

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    answers = AnswerSerializer(many=True, required=False)
    user = serializers.StringRelatedField()
    class Meta:
        model = Question
        fields = ['url','user', 'title', 'body', 'answers',]