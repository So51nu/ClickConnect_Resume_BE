from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import User, OTP
from .serializers import UserSerializer
import random


# ================== SEND OTP ==================

class SendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get("phone")

        if not phone:
            return Response({"message": "Phone required"}, status=400)

        otp_code = str(random.randint(100000, 999999))
        OTP.objects.create(phone=phone, code=otp_code)

        print("OTP (DEV):", otp_code)

        return Response({
            "is_registered": User.objects.filter(phone=phone).exists()
        })


# ================== VERIFY OTP ==================
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, OTP

from .models import User, OTP
from .serializers import UserSerializer
import random


# ================== SEND OTP ==================
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get("phone")
        otp = request.data.get("otp")

        if not phone or not otp:
            return Response({"message": "Phone and OTP are required"}, status=400)

        otp_obj = OTP.objects.filter(phone=phone, code=otp).last()
        if not otp_obj or not otp_obj.is_valid():
            return Response({"message": "Invalid OTP"}, status=400)

        user = User.objects.filter(phone=phone).first()

        # 🔹 AUTO DECIDE: REGISTER or LOGIN
        if not user:
            user = User.objects.create(
                phone=phone,
                name=request.data.get("name", ""),
                email=request.data.get("email", ""),
                pincode=request.data.get("pincode", ""),
            )
            action = "registered"
        else:
            action = "logged_in"

        otp_obj.delete()

        refresh = RefreshToken.for_user(user)

        return Response({
            "action": action,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "phone": user.phone,
                "name": user.name,
                "email": user.email,
                "pincode": user.pincode,
            }
        })

# ================== ADMIN LOGIN ==================

class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get("phone")
        password = request.data.get("password")

        user = authenticate(phone=phone, password=password)

        if not user or not user.is_staff:
            return Response(
                {"error": "Invalid admin credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "phone": user.phone,
                "name": user.name,
                "role": "admin",
            }
        })


# ================== ADMIN USER LIST ==================

class AdminUserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.filter(is_staff=False).order_by("-date_joined")
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


# ================== ADMIN USER DETAIL ==================

class AdminUserDetailView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk, is_staff=False)
            user.delete()
            return Response({"message": "User deleted"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
