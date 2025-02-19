from django.urls import path, include
from rest_framework_nested import routers
from .views import UserViewSet, ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'conversations', ConversationViewSet, basename='conversation')  # Plural name

# Nested router for messages under conversations
nested_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')  # Plural name

urlpatterns = [
    path('chat/', include(router.urls)),
    path('chat/', include(nested_router.urls)),  # Include nested routes
]
