# # from rest_framework.views import APIView
# # from rest_framework.response import Response
# # from rest_framework.permissions import AllowAny, IsAdminUser
# # from rest_framework import status
# # from rest_framework_simplejwt.tokens import RefreshToken
# # from django.contrib.auth import authenticate

# # from .models import User, OTP
# # from .serializers import UserSerializer
# # import random


# # # ================== SEND OTP ==================

# # class SendOTPView(APIView):
# #     permission_classes = [AllowAny]

# #     def post(self, request):
# #         phone = request.data.get("phone")

# #         if not phone:
# #             return Response({"message": "Phone required"}, status=400)

# #         otp_code = str(random.randint(100000, 999999))
# #         OTP.objects.create(phone=phone, code=otp_code)

# #         print("OTP (DEV):", otp_code)

# #         return Response({
# #             "is_registered": User.objects.filter(phone=phone).exists()
# #         })


# # # ================== VERIFY OTP ==================
# # from django.utils import timezone
# # from rest_framework.views import APIView
# # from rest_framework.response import Response
# # from rest_framework.permissions import AllowAny
# # from rest_framework_simplejwt.tokens import RefreshToken
# # from .models import User, OTP

# # from .models import User, OTP
# # from .serializers import UserSerializer
# # import random


# # # ================== SEND OTP ==================
# # class VerifyOTPView(APIView):
# #     permission_classes = [AllowAny]

# #     def post(self, request):
# #         phone = request.data.get("phone")
# #         otp = request.data.get("otp")

# #         if not phone or not otp:
# #             return Response({"message": "Phone and OTP are required"}, status=400)

# #         otp_obj = OTP.objects.filter(phone=phone, code=otp).last()
# #         if not otp_obj or not otp_obj.is_valid():
# #             return Response({"message": "Invalid OTP"}, status=400)

# #         user = User.objects.filter(phone=phone).first()

# #         # 🔹 AUTO DECIDE: REGISTER or LOGIN
# #         if not user:
# #             user = User.objects.create(
# #                 phone=phone,
# #                 name=request.data.get("name", ""),
# #                 email=request.data.get("email", ""),
# #                 pincode=request.data.get("pincode", ""),
# #             )
# #             action = "registered"
# #         else:
# #             action = "logged_in"

# #         otp_obj.delete()

# #         refresh = RefreshToken.for_user(user)

# #         return Response({
# #             "action": action,
# #             "access": str(refresh.access_token),
# #             "refresh": str(refresh),
# #             "user": {
# #                 "phone": user.phone,
# #                 "name": user.name,
# #                 "email": user.email,
# #                 "pincode": user.pincode,
# #             }
# #         })

# # # ================== ADMIN LOGIN ==================

# # class AdminLoginView(APIView):
# #     permission_classes = [AllowAny]

# #     def post(self, request):
# #         phone = request.data.get("phone")
# #         password = request.data.get("password")

# #         user = authenticate(phone=phone, password=password)

# #         if not user or not user.is_staff:
# #             return Response(
# #                 {"error": "Invalid admin credentials"},
# #                 status=status.HTTP_401_UNAUTHORIZED
# #             )

# #         refresh = RefreshToken.for_user(user)

# #         return Response({
# #             "access": str(refresh.access_token),
# #             "refresh": str(refresh),
# #             "user": {
# #                 "id": user.id,
# #                 "phone": user.phone,
# #                 "name": user.name,
# #                 "role": "admin",
# #             }
# #         })


# # # ================== ADMIN USER LIST ==================

# # class AdminUserListView(APIView):
# #     permission_classes = [IsAdminUser]

# #     def get(self, request):
# #         users = User.objects.filter(is_staff=False).order_by("-date_joined")
# #         serializer = UserSerializer(users, many=True)
# #         return Response(serializer.data)


# # # ================== ADMIN USER DETAIL ==================

# # class AdminUserDetailView(APIView):
# #     permission_classes = [IsAdminUser]

# #     def delete(self, request, pk):
# #         try:
# #             user = User.objects.get(pk=pk, is_staff=False)
# #             user.delete()
# #             return Response({"message": "User deleted"})
# #         except User.DoesNotExist:
# #             return Response({"error": "User not found"}, status=404)
# # views.py
# import random
# from django.contrib.auth import authenticate
# from rest_framework import status
# from rest_framework.permissions import AllowAny, IsAdminUser
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken

# from .models import User, OTP
# from .serializers import UserSerializer


# # ================== SEND OTP ==================
# class SendOTPView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         phone = request.data.get("phone")
#         if not phone:
#             return Response({"message": "Phone required"}, status=400)

#         otp_code = str(random.randint(100000, 999999))
#         OTP.objects.create(phone=phone, code=otp_code)

#         # DEV only
#         print("OTP (DEV):", otp_code)

#         return Response({"is_registered": User.objects.filter(phone=phone).exists()})


# # ================== VERIFY OTP ==================
# class VerifyOTPView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         phone = request.data.get("phone")
#         # support both "otp" and "code" from frontend
#         otp_value = request.data.get("otp") or request.data.get("code")

#         if not phone or not otp_value:
#             return Response({"message": "Phone and OTP are required"}, status=400)

#         otp_obj = OTP.objects.filter(phone=phone, code=otp_value).last()
#         if not otp_obj or not otp_obj.is_valid():
#             return Response({"message": "Invalid OTP"}, status=400)

#         user = User.objects.filter(phone=phone).first()

#         if not user:
#             user = User.objects.create(
#                 phone=phone,
#                 name=request.data.get("name", ""),
#                 email=request.data.get("email", ""),
#                 pincode=request.data.get("pincode", ""),
#                 is_staff=False,
#             )
#             user.set_unusable_password()
#             user.save()
#             action = "registered"
#         else:
#             action = "logged_in"

#         otp_obj.delete()
#         refresh = RefreshToken.for_user(user)

#         return Response({
#             "action": action,
#             "access": str(refresh.access_token),
#             "refresh": str(refresh),
#             "user": {
#                 "id": user.id,
#                 "phone": user.phone,
#                 "name": user.name,
#                 "email": user.email,
#                 "pincode": user.pincode,
#             }
#         })


# # ================== ADMIN LOGIN ==================
# class AdminLoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         phone = request.data.get("phone")
#         password = request.data.get("password")

#         user = authenticate(phone=phone, password=password)
#         if not user or not user.is_staff:
#             return Response({"error": "Invalid admin credentials"}, status=status.HTTP_401_UNAUTHORIZED)

#         refresh = RefreshToken.for_user(user)

#         return Response({
#             "access": str(refresh.access_token),
#             "refresh": str(refresh),
#             "user": {
#                 "id": user.id,
#                 "phone": user.phone,
#                 "name": user.name,
#                 "role": "admin",
#             }
#         })


# # ================== ADMIN USER LIST (GET + POST) ==================
# class AdminUserListView(APIView):
#     permission_classes = [IsAdminUser]

#     def get(self, request):
#         users = User.objects.filter(is_staff=False).order_by("-date_joined")
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         # create student/user
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save(is_staff=False)
#             return Response(UserSerializer(user).data, status=201)
#         return Response(serializer.errors, status=400)


# # ================== ADMIN USER DETAIL (GET + PATCH/PUT + DELETE) ==================
# class AdminUserDetailView(APIView):
#     permission_classes = [IsAdminUser]

#     def get(self, request, pk):
#         try:
#             user = User.objects.get(pk=pk, is_staff=False)
#             return Response(UserSerializer(user).data)
#         except User.DoesNotExist:
#             return Response({"error": "User not found"}, status=404)

#     def patch(self, request, pk):
#         try:
#             user = User.objects.get(pk=pk, is_staff=False)
#             serializer = UserSerializer(user, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=400)
#         except User.DoesNotExist:
#             return Response({"error": "User not found"}, status=404)

#     def put(self, request, pk):
#         # full update
#         try:
#             user = User.objects.get(pk=pk, is_staff=False)
#             serializer = UserSerializer(user, data=request.data, partial=False)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=400)
#         except User.DoesNotExist:
#             return Response({"error": "User not found"}, status=404)

#     def delete(self, request, pk):
#         try:
#             user = User.objects.get(pk=pk, is_staff=False)
#             user.delete()
#             return Response({"message": "User deleted"})
#         except User.DoesNotExist:
#             return Response({"error": "User not found"}, status=404)

import random
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics

from .models import User, OTP, ResumeTemplate, TemplatePricing
from .serializers import (
    UserSerializer,
    ResumeTemplateSerializer,
    TemplatePricingSerializer,
)


# ================== SEND OTP ==================
class SendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get("phone")
        if not phone:
            return Response({"message": "Phone required"}, status=400)

        otp_code = str(random.randint(100000, 999999))
        OTP.objects.create(phone=phone, code=otp_code)

        # DEV only
        print("OTP (DEV):", otp_code)

        return Response({"is_registered": User.objects.filter(phone=phone).exists()})


# ================== VERIFY OTP ==================
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get("phone")
        otp_value = request.data.get("otp") or request.data.get("code")

        if not phone or not otp_value:
            return Response({"message": "Phone and OTP are required"}, status=400)

        otp_obj = OTP.objects.filter(phone=phone, code=otp_value).last()
        if not otp_obj or not otp_obj.is_valid():
            return Response({"message": "Invalid OTP"}, status=400)

        user = User.objects.filter(phone=phone).first()

        if not user:
            user = User.objects.create(
                phone=phone,
                name=request.data.get("name", ""),
                email=request.data.get("email", ""),
                pincode=request.data.get("pincode", ""),
                is_staff=False,
            )
            user.set_unusable_password()
            user.save()
            action = "registered"
        else:
            action = "logged_in"

        otp_obj.delete()

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "action": action,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "phone": user.phone,
                    "name": user.name,
                    "email": user.email,
                    "pincode": user.pincode,
                },
            }
        )


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
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {"id": user.id, "phone": user.phone, "name": user.name, "role": "admin"},
            }
        )


# ================== ADMIN USERS (CRUD) ==================
class AdminUserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.filter(is_staff=False).order_by("-date_joined")
        return Response(UserSerializer(users, many=True).data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_staff=False)
            return Response(UserSerializer(user).data, status=201)
        return Response(serializer.errors, status=400)


class AdminUserDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk, is_staff=False)
            return Response(UserSerializer(user).data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk, is_staff=False)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk, is_staff=False)
            serializer = UserSerializer(user, data=request.data, partial=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk, is_staff=False)
            user.delete()
            return Response({"message": "User deleted"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)


# =========================
# ✅ NEW: Admin Templates APIs
# =========================

class AdminTemplateListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = ResumeTemplate.objects.all().order_by("-updated_at")
    serializer_class = ResumeTemplateSerializer


class AdminTemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = ResumeTemplate.objects.all()
    serializer_class = ResumeTemplateSerializer


# =========================
# ✅ NEW: Admin Template Pricing APIs
# =========================

class AdminTemplatePricingListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = TemplatePricing.objects.select_related("template").all().order_by("-updated_at")
    serializer_class = TemplatePricingSerializer


class AdminTemplatePricingDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = TemplatePricing.objects.select_related("template").all()
    serializer_class = TemplatePricingSerializer

# views.py (subscription section ko replace/add karo)
from django.db.models import Sum, Q
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Subscription
from .serializers import SubscriptionSerializer


class AdminSubscriptionListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = Subscription.objects.select_related("user").order_by("-created_at")

        plan = request.GET.get("plan")
        st = request.GET.get("status")
        search = request.GET.get("search")

        if plan:
            qs = qs.filter(plan=plan)
        if st:
            qs = qs.filter(status=st)

        if search:
            search = search.strip()
            qs = qs.filter(
                Q(user__name__icontains=search)
                | Q(user__email__icontains=search)
                | Q(user__phone__icontains=search)
            )

        serializer = SubscriptionSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            sub = serializer.save()
            return Response(SubscriptionSerializer(sub).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminSubscriptionDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        return Subscription.objects.select_related("user").get(pk=pk)

    def get(self, request, pk):
        try:
            sub = self.get_object(pk)
            return Response(SubscriptionSerializer(sub).data)
        except Subscription.DoesNotExist:
            return Response({"error": "Subscription not found"}, status=404)

    def patch(self, request, pk):
        try:
            sub = self.get_object(pk)
            serializer = SubscriptionSerializer(sub, data=request.data, partial=True)
            if serializer.is_valid():
                sub = serializer.save()
                return Response(SubscriptionSerializer(sub).data)
            return Response(serializer.errors, status=400)
        except Subscription.DoesNotExist:
            return Response({"error": "Subscription not found"}, status=404)

    def put(self, request, pk):
        try:
            sub = self.get_object(pk)
            serializer = SubscriptionSerializer(sub, data=request.data, partial=False)
            if serializer.is_valid():
                sub = serializer.save()
                return Response(SubscriptionSerializer(sub).data)
            return Response(serializer.errors, status=400)
        except Subscription.DoesNotExist:
            return Response({"error": "Subscription not found"}, status=404)

    def delete(self, request, pk):
        try:
            sub = self.get_object(pk)
            sub.delete()
            return Response({"message": "Subscription deleted"})
        except Subscription.DoesNotExist:
            return Response({"error": "Subscription not found"}, status=404)


class AdminSubscriptionStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total = Subscription.objects.count()
        active = Subscription.objects.filter(status="Active").count()

        revenue = Subscription.objects.filter(status="Active").aggregate(total=Sum("amount"))["total"] or 0

        churn = 0
        if total:
            churn = round((Subscription.objects.filter(status="Cancelled").count() / total) * 100, 2)

        return Response({
            "total": total,
            "active": active,
            "revenue": revenue,
            "churn": churn,
        })
