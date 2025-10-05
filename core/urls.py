from django.urls import path
from . import views

urlpatterns = [
    path('recordings/', views.recording_create, name='recording-create'),
    path('recordings/list/', views.recording_list, name='recording-list'),
    path('alerts/', views.get_alerts, name='get-alerts'),
]
