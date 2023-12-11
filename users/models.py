from django.contrib.auth.hashers import make_password
from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError
from django.utils.crypto import get_random_string
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


ROLES = (
    ("Admin", "Admin"),
    ("Student", "Student"),
    ("Librarian", "Librarian")
)


class Group(models.Model):
    title = models.CharField(max_length=150)

    class Meta:
        db_table = "group"

    def __str__(self):
        return f"{self.title} group"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required field")

        email = self.normalize_email(email)
        role = extra_fields.get("role", "Student")

        if role not in dict(ROLES).values():
            raise ValueError("Invalid user status")

        user = self.model(email=email, **extra_fields)
        user.role = role
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields["role"] = "Admin"

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    password = models.CharField(max_length=150)
    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=150, null=True)
    role = models.CharField(max_length=150, choices=ROLES, default=ROLES[1][1])
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)

    username = None
    date_joined = None
    last_login = None
    groups = None
    user_permissions = None
    first_name = None
    last_name = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.role} {self.firstname} {self.lastname}"

    def save(self, *args, **kwargs):
        if self.role != ROLES[1][1]:
            self.group = None
        self.password = make_password(self.password)
        super().save()
