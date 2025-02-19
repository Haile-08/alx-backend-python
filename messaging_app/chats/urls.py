from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'conversation', ConversationViewSet, basename='conversation')

# create a nested route for message
nested_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested_router.register(r'message', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('chat/', include(router.urls))
]