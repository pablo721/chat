from django.urls import path, include
from rest_framework import routers
from . import views2 as views


router = routers.DefaultRouter()
router.register(r'messages', views.MessageViewSet, basename='messages')
router.register(r'chat', views.ChatViewSet, basename='chat')

#router.register(r'users', views.UsersView)
#router.register(r'monitor', views.MonitorView)

app_name = 'api'
urlpatterns = [
	path('', include(router.urls)),
]


