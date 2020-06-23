"""questionbox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from core import views as core_views
from api import views as api_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', api_views.UserViewSet)
router.register('questions', api_views.QuestionViewSet, basename='question')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('registration.backends.simple.urls')),
    path('', core_views.homepage, name='homepage'),
    path('questions/', core_views.list_questions, name='question_list'),
    path('questions/<int:question_pk>/detail/', core_views.question_detail, name='question_detail'),
    path('questions/new/', core_views.ask_question, name='ask_question'),
    path('questions/<int:question_pk>/edit/', core_views.edit_question, name='edit_question'),
    path('questions/<int:question_pk>/delete/', core_views.delete_question, name='delete_question'),
    path('questions/<int:question_pk>/star/', core_views.toggle_star_question, name='toggle_star_question'),
    path('questions/<int:question_pk>/answer_question/', core_views.answer_question, 
    name='answer_question'),
    path('questions/<int:question_pk>/<int:answer_pk>/mark_correct/', core_views.mark_answer_correct, name='mark_correct'),
    path('questions/search/', core_views.search_questions, name='search_questions'),
    path('user/profile', core_views.user_profile, name='user_profile'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
