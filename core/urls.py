from django.urls import path
from . import views

urlpatterns = [
    path('recordings/', views.recording_create, name='recording-create'),
]
