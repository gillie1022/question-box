from rest_framework import serializers
from users.models import User
from core.models import Question, Answer

class UserSerializer(serializers.HyperlinkedModelSerializer):
    questions = serializers.PrimaryKeyRelatedField(many=True, queryset=Question.objects.all())
    answers = serializers.PrimaryKeyRelatedField(many=True, queryset=Answer.objects.all())
    
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'is_staff', 'questions', 'answers']

class AnswerSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    
    class Meta:
        model = Answer
        fields = ['author', 'body', 'answered_on', "marked_correct",]

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    answers = AnswerSerializer(many=True, required=False)
    user = serializers.StringRelatedField()

    def create(self, validated_data):
        answers = validated_data.pop('answers', [])
        question = Question.objects.create(**validated_data)
        for answer in answers:
            question.answers.create(**answer)
        return question

    class Meta:
        model = Question
        fields = ['url', 'user', 'title', 'body', 'answers',]