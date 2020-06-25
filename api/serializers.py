from rest_framework import serializers
from users.models import User
from core.models import Question, Answer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    questions = serializers.StringRelatedField(many=True)
    answers = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ["id", "url", "username", "email", "is_staff", "questions", "answers"]


class AnswerSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    marked_correct = serializers.BooleanField(read_only=True)

    class Meta:
        model = Answer
        fields = [
            "question",
            "author",
            "body",
            "answered_on",
            "marked_correct",
        ]


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    answers = AnswerSerializer(many=True, required=False, read_only=True)
    user = serializers.StringRelatedField()
    starred_by = serializers.StringRelatedField(many=True, read_only=True)

    def create(self, validated_data):
        answers = validated_data.pop("answers", [])
        starred_by = validated_data.pop("starred_by", [])
        question = Question.objects.create(**validated_data)
        for answer in answers:
            question.answers.create(**answer)
        for star in starred_by:
            question.starred_by.create(**star)
        return question

    def update(self, instance, validated_data):
        question = instance
        answers = validated_data.pop("answers", [])
        starred_by = validated_data.pop("starred_by", [])
        for key, value in validated_data.items():
            setattr(question, key, value)
        question.save()

        question.answers.all().delete()
        for answer in answers:
            question.answers.create(**answer)
        question.starred_by.all().delete()
        for star in starred_by:
            question.starred_by.create(**star)
        return question

    class Meta:
        model = Question
        fields = ["url", "user", "title", "body", "answers", "starred_by"]

