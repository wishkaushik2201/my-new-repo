from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-id')  # safer than created_at if missing

    def create(self, request, *args, **kwargs):
        # Registration
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email and password required"}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=400)

        if check_password(password, user.password):
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            serializer = self.get_serializer(user)

            # ✅ Create response
            response = Response({
                "message": "Login successful",
                "user": serializer.data,
            }, status=200)

            # ✅ Store tokens in httpOnly cookies
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,   # cannot be accessed via JS
                secure=False,    # set True in production (HTTPS only)
                samesite="Lax"
            )
            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=False,
                samesite="Lax"
            )

            return response

        return Response({"error": "Invalid credentials"}, status=400)

    @action(detail=False, methods=['get'], url_path='by-username')
    def by_username(self, request):
        username = request.query_params.get('username')
        if not username:
            return Response({'detail': 'username query param required'}, status=400)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': 'not found'}, status=404)
        serializer = self.get_serializer(user)
        return Response(serializer.data)
