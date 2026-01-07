# # from rest_framework import serializers
# # from .models import User, OTP


# # class UserSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = User
# #         fields = [
# #             "id",
# #             "phone",
# #             "name",
# #             "email",
# #             "pincode",
# #             "-created_at",
# #         ]


# # class OTPSendSerializer(serializers.Serializer):
# #     phone = serializers.CharField(max_length=10)


# # class OTPVerifySerializer(serializers.Serializer):
# #     phone = serializers.CharField(max_length=10)
# #     code = serializers.CharField(max_length=6)

# # serializers.py
# from rest_framework import serializers
# from .models import User, OTP


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = [
#             "id",
#             "phone",
#             "name",
#             "email",
#             "pincode",
#             "date_joined",
#         ]
#         read_only_fields = ["id", "date_joined"]

#     def create(self, validated_data):
#         # For OTP-based users: no password needed
#         user = User.objects.create(**validated_data)
#         user.set_unusable_password()
#         user.save()
#         return user


# class OTPSendSerializer(serializers.Serializer):
#     phone = serializers.CharField(max_length=10)


# class OTPVerifySerializer(serializers.Serializer):
#     phone = serializers.CharField(max_length=10)
#     code = serializers.CharField(max_length=6)

from rest_framework import serializers
from .models import User, OTP, ResumeTemplate, TemplatePricing


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone", "name", "email", "pincode", "date_joined"]
        read_only_fields = ["id", "date_joined"]

    def create(self, validated_data):
        # OTP-based users: password not needed
        user = User.objects.create(**validated_data)
        user.set_unusable_password()
        user.save()
        return user


class OTPSendSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=10)


class OTPVerifySerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=10)
    code = serializers.CharField(max_length=6)


# =========================
# ✅ NEW: Templates + Pricing serializers
# =========================

# class ResumeTemplateSerializer(serializers.ModelSerializer):
#     updated = serializers.SerializerMethodField()

#     class Meta:
#         model = ResumeTemplate
#         fields = [
#             "id",
#             "name",
#             "category",
#             "layout",
#             "status",
#             "downloads",
#             "rating",
#             "color",
#             "updated",
#             "updated_at",
#             "created_at",
#         ]
#         read_only_fields = ["id", "updated", "updated_at", "created_at"]

#     def get_updated(self, obj):
#         # frontend wants dd/mm/yyyy
#         return obj.updated_at.strftime("%d/%m/%Y")


# class TemplatePricingSerializer(serializers.ModelSerializer):
#     templateName = serializers.CharField(source="template.name", read_only=True)
#     template_id = serializers.PrimaryKeyRelatedField(
#         source="template", queryset=ResumeTemplate.objects.all(), write_only=True
#     )
#     updated = serializers.SerializerMethodField()

#     class Meta:
#         model = TemplatePricing
#         fields = [
#             "id",
#             "template_id",
#             "templateName",
#             "billing_type",
#             "currency",
#             "price",
#             "discount_percent",
#             "final_price",
#             "status",
#             "updated",
#             "updated_at",
#             "created_at",
#         ]
#         read_only_fields = ["id", "templateName", "final_price", "updated", "updated_at", "created_at"]

#     def get_updated(self, obj):
#         return obj.updated_at.strftime("%d/%m/%Y")

# serializers.py
from rest_framework import serializers
from .models import ResumeTemplate, TemplatePricing

class ResumeTemplateSerializer(serializers.ModelSerializer):
    updated = serializers.SerializerMethodField()

    class Meta:
        model = ResumeTemplate
        fields = [
            "id",
            "name",
            "category",
            "layout",
            "status",
            "downloads",
            "rating",
            "color",

            # ✅ NEW
            "source",
            "description",
            "schema",
            "preview_image",
            "version",

            "updated",
            "updated_at",
            "created_at",
        ]
        read_only_fields = ["id", "updated", "updated_at", "created_at", "version"]

    def get_updated(self, obj):
        return obj.updated_at.strftime("%d/%m/%Y")


class TemplatePricingSerializer(serializers.ModelSerializer):
    templateName = serializers.CharField(source="template.name", read_only=True)

    # ✅ write-only (already)
    template_id = serializers.PrimaryKeyRelatedField(
        source="template", queryset=ResumeTemplate.objects.all(), write_only=True
    )

    # ✅ read-only - frontend edit ke liye
    template_pk = serializers.IntegerField(source="template.id", read_only=True)

    updated = serializers.SerializerMethodField()

    class Meta:
        model = TemplatePricing
        fields = [
            "id",
            "template_id",
            "template_pk",
            "templateName",
            "billing_type",
            "currency",
            "price",
            "discount_percent",
            "final_price",
            "status",
            "updated",
            "updated_at",
            "created_at",
        ]
        read_only_fields = ["id", "templateName", "template_pk", "final_price", "updated", "updated_at", "created_at"]

    def get_updated(self, obj):
        return obj.updated_at.strftime("%d/%m/%Y")


# serializers.py

from .models import Subscription
class SubscriptionSerializer(serializers.ModelSerializer):
    # display fields for table
    user_name = serializers.CharField(source="user.name", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)
    user_phone = serializers.CharField(source="user.phone", read_only=True)

    # write field for create/update
    user_id = serializers.PrimaryKeyRelatedField(
        source="user",
        queryset=User.objects.filter(is_staff=False),
        write_only=True,
        required=True,
    )

    class Meta:
        model = Subscription
        fields = [
            "id",
            "user_id",
            "user_name",
            "user_email",
            "user_phone",
            "plan",
            "amount",
            "status",
            "start_date",
            "end_date",
            "auto_renew",
            "created_at",
        ]
        read_only_fields = ["id", "user_name", "user_email", "user_phone", "created_at"]
        