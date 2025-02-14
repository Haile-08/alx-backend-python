from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ConversationViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'conversation', ConversationViewSet, basename='conversation')

urlpatterns = router.urls