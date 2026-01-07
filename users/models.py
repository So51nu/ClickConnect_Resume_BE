# from django.db import models
# from django.contrib.auth.models import (
#     AbstractBaseUser,
#     PermissionsMixin,
#     BaseUserManager,
# )
# from django.utils import timezone


# class UserManager(BaseUserManager):
#     def create_user(self, phone, password=None, **extra_fields):
#         if not phone:
#             raise ValueError("Phone number is required")

#         user = self.model(phone=phone, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, phone, password, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)
#         return self.create_user(phone, password, **extra_fields)


# class User(AbstractBaseUser, PermissionsMixin):
#     phone = models.CharField(max_length=10, unique=True)
#     name = models.CharField(max_length=100, blank=True)
#     email = models.EmailField(blank=True)
#     pincode = models.CharField(max_length=6, blank=True)

#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     date_joined = models.DateTimeField(default=timezone.now)

#     # 🔥 IMPORTANT FIX (NO MORE CLASH)
#     groups = models.ManyToManyField(
#         "auth.Group",
#         related_name="users_custom",
#         blank=True,
#     )
#     user_permissions = models.ManyToManyField(
#         "auth.Permission",
#         related_name="users_custom_permissions",
#         blank=True,
#     )

#     objects = UserManager()

#     USERNAME_FIELD = "phone"
#     REQUIRED_FIELDS = []

#     def __str__(self):
#         return self.phone
# class OTP(models.Model):
#     phone = models.CharField(max_length=10)
#     code = models.CharField(max_length=6)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def is_valid(self):
#         return (timezone.now() - self.created_at).seconds < 300

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Phone number is required")

        user = self.model(phone=phone, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    pincode = models.CharField(max_length=6, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    # ✅ avoid reverse accessor clash
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="users_custom",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="users_custom_permissions",
        blank=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone


class OTP(models.Model):
    phone = models.CharField(max_length=10)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # valid for 5 mins
        return (timezone.now() - self.created_at).total_seconds() < 300


# =========================
# ✅ NEW: Templates + Pricing
# =========================

# class ResumeTemplate(models.Model):
#     STATUS_CHOICES = (("active", "Active"), ("draft", "Draft"))
#     CATEGORY_CHOICES = (("Modern", "Modern"), ("Classic", "Classic"))
#     LAYOUT_CHOICES = (
#         ("Two Column", "Two Column"),
#         ("Single Column", "Single Column"),
#         ("Sidebar Left", "Sidebar Left"),
#         ("Sidebar Right", "Sidebar Right"),
#     )

#     name = models.CharField(max_length=150, unique=True)
#     category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default="Modern")
#     layout = models.CharField(max_length=30, choices=LAYOUT_CHOICES, default="Two Column")
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")

#     downloads = models.PositiveIntegerField(default=0)
#     rating = models.FloatField(default=0)
#     color = models.CharField(max_length=30, default="#2563eb")

#     updated_at = models.DateTimeField(auto_now=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


# class TemplatePricing(models.Model):
#     STATUS_CHOICES = (("active", "Active"), ("inactive", "Inactive"))
#     BILLING_CHOICES = (("free", "Free"), ("one_time", "One-time"), ("subscription", "Subscription"))
#     CURRENCY_CHOICES = (("INR", "INR"), ("USD", "USD"))

#     template = models.OneToOneField(ResumeTemplate, on_delete=models.CASCADE, related_name="pricing")

#     billing_type = models.CharField(max_length=20, choices=BILLING_CHOICES, default="one_time")
#     currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="INR")

#     price = models.FloatField(default=0)
#     discount_percent = models.FloatField(default=0)
#     final_price = models.FloatField(default=0)

#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")

#     updated_at = models.DateTimeField(auto_now=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def _calc_final(self):
#         p = float(self.price or 0)
#         d = float(self.discount_percent or 0)
#         if self.billing_type == "free":
#             return 0.0
#         final = p - (p * d / 100.0)
#         return round(final, 2)

#     def save(self, *args, **kwargs):
#         # normalize for free
#         if self.billing_type == "free":
#             self.price = 0
#             self.discount_percent = 0
#         self.final_price = self._calc_final()
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.template.name} pricing"

# models.py

class Subscription(models.Model):
    PLAN_CHOICES = (
        ("Pro", "Pro"),
        ("Enterprise", "Enterprise"),
    )

    STATUS_CHOICES = (
        ("Active", "Active"),
        ("Cancelled", "Cancelled"),
        ("Expired", "Expired"),
        ("Past Due", "Past Due"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    amount = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    auto_renew = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.phone} - {self.plan}"


# models.py
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class ResumeTemplate(models.Model):
    STATUS_CHOICES = (("active", "Active"), ("draft", "Draft"))
    CATEGORY_CHOICES = (("Modern", "Modern"), ("Classic", "Classic"))
    LAYOUT_CHOICES = (
        ("Two Column", "Two Column"),
        ("Single Column", "Single Column"),
        ("Sidebar Left", "Sidebar Left"),
        ("Sidebar Right", "Sidebar Right"),
    )
    SOURCE_CHOICES = (
        ("custom", "Custom"),
        ("imported", "Imported"),
        ("duplicated", "Duplicated"),
    )

    name = models.CharField(max_length=150, unique=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default="Modern")
    layout = models.CharField(max_length=30, choices=LAYOUT_CHOICES, default="Two Column")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")

    downloads = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=0)
    color = models.CharField(max_length=30, default="#2563eb")

    # ✅ NEW (Template Clone Architecture)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default="custom")
    description = models.TextField(blank=True, default="")
    schema = models.JSONField(default=dict, blank=True)  # ✅ main template JSON
    preview_image = models.FileField(upload_to="templates/previews/", null=True, blank=True)  # ✅ stored in our media

    version = models.PositiveIntegerField(default=1)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # def delete(self, *args, **kwargs):
    #     # ✅ delete stored preview file from our storage (freeze assets cleanup)
    #     if self.preview_image:
    #         try:
    #             self.preview_image.delete(save=False)
    #         except Exception:
    #             pass
    #     super().delete(*args, **kwargs)
    def delete(self, *args, **kwargs):
    # ✅ delete stored preview file from storage
        if self.preview_image:
            try:
                self.preview_image.delete(save=False)
            except Exception:
                pass

        return super().delete(*args, **kwargs)


    def __str__(self):
        return self.name


class TemplatePricing(models.Model):
    STATUS_CHOICES = (("active", "Active"), ("inactive", "Inactive"))
    BILLING_CHOICES = (("free", "Free"), ("one_time", "One-time"), ("subscription", "Subscription"))
    CURRENCY_CHOICES = (("INR", "INR"), ("USD", "USD"))

    template = models.OneToOneField(ResumeTemplate, on_delete=models.CASCADE, related_name="pricing")

    billing_type = models.CharField(max_length=20, choices=BILLING_CHOICES, default="one_time")
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="INR")

    price = models.FloatField(default=0)
    discount_percent = models.FloatField(default=0)
    final_price = models.FloatField(default=0)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _calc_final(self):
        p = float(self.price or 0)
        d = float(self.discount_percent or 0)
        if self.billing_type == "free":
            return 0
        if d <= 0:
            return p
        return max(0, p - (p * d / 100.0))

    def save(self, *args, **kwargs):
        if self.billing_type == "free":
            self.price = 0
            self.discount_percent = 0
        self.final_price = self._calc_final()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.template.name} pricing"


# ✅ Auto create default FREE pricing on every template creation/import/duplicate
@receiver(post_save, sender=ResumeTemplate)
def create_default_pricing(sender, instance: ResumeTemplate, created, **kwargs):
    if created:
        TemplatePricing.objects.get_or_create(
            template=instance,
            defaults={
                "billing_type": "free",
                "currency": "INR",
                "price": 0,
                "discount_percent": 0,
                "status": "active",
            },
        )


