from django.urls import path, include
from . import views

urlpatterns = [
    path('create-event/', views.create_event, name='create_event'),
    path('api/events/<int:event_id>/qr/', views.get_event_qrcode, name='event-qr'),
    path('check-in/', views.check_in, name='check_in'),
]