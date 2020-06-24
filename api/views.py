from django.shortcuts import render
from rest_framework import viewsets, permissions
from users.models import User
from core.models import Question
from api.serializers import UserSerializer, QuestionSerializer, AnswerSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)