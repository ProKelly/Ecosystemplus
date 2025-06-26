from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import action
from api.serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserSerializer,
    CommunitySerializer, AdminAccessRequestSerializer, AdminAccessReviewSerializer,
    CustomTokenObtainPairSerializer
)
from base.models import User, Community, AdminAccessRequest


# -------------------- AUTH & PROFILE -------------------- #

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT login view using email instead of username.
    """
    serializer_class = CustomTokenObtainPairSerializer


# -------------------- CUSTOM PERMISSIONS -------------------- #

class IsCommunityAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'community'


# -------------------- COMMUNITY VIEWSET -------------------- #

class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsCommunityAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(admin=self.request.user)

    @action(detail=False, methods=['get'], url_path='my')
    def my_community(self, request):
        """
        Returns the community for which the current user is the admin.
        """
        try:
            community = Community.objects.get(admin=request.user)
            serializer = self.get_serializer(community)
            return Response(serializer.data)
        except Community.DoesNotExist:
            return Response({'detail': 'No community found for this admin.'}, status=status.HTTP_404_NOT_FOUND)


# -------------------- ADMIN ACCESS REQUEST VIEWSET -------------------- #

class AdminAccessRequestViewSet(viewsets.ModelViewSet):
    queryset = AdminAccessRequest.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return AdminAccessRequest.objects.all()
        return AdminAccessRequest.objects.filter(user=user)

    def get_serializer_class(self):
        if self.request.user.is_admin:
            return AdminAccessReviewSerializer
        return AdminAccessRequestSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
