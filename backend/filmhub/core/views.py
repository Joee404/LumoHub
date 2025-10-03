from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer

class RegisterView(APIView):
    """
    API endpoint to register a new user.

    Method: POST
    URL: /register/

    Expected request data (JSON):
    {
        "username": "your_username",
        "email": "your_email@example.com",
        "password": "your_password",
        "confirm_password": "your_password"
    }

    Responses:
    - 201 Created: User registered successfully
    - 400 Bad Request: Validation errors
    """
    
    def post(self, request):
        """
        Handles POST requests to register a user.
        Uses RegisterSerializer to validate input and save user to database.
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(TokenObtainPairView):
    """
    API endpoint to login a user using JWT.

    Method: POST
    URL: /login/

    Expected request data (JSON):
    {
        "username": "your_username",
        "password": "your_password"
    }

    Responses:
    - 200 OK: Returns access and refresh JWT tokens
    - 401 Unauthorized: Invalid credentials
    """
    serializer_class = LoginSerializer

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
