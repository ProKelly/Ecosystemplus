from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

from api.views import (
    UserRegistrationView, UserProfileView,
    CommunityViewSet, AdminAccessRequestViewSet,
    CustomTokenObtainPairView  # use this instead of default login
)

router = DefaultRouter()
router.register(r'communities', CommunityViewSet, basename='community')
router.register(r'admin-access-requests', AdminAccessRequestViewSet, basename='admin-access')

urlpatterns = [
    # Auth
    path('auth/register/', UserRegistrationView.as_view(), name='user-register'),
    path('auth/token/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),  # JWT login
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token-verify'),
    path('auth/profile/', UserProfileView.as_view(), name='user-profile'),

    # ViewSets
    path('', include(router.urls)),
]
