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


def check_email_exist(email: str):
    if not email:
        raise ValueError("Email is required field")


def check_role_exist(role: str):
    if role not in dict(ROLES).values():
        raise ValueError("Invalid user role")


def set_password_exist(self, password):
    if not password:
        self.set_password(password)


def validate_phone(phone: str):
    if not phone.isdigit():
        raise ValueError("Invalid phone number")


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):

        check_email_exist(email)

        email = self.normalize_email(email)
        role = extra_fields.get("role", "Student")

        check_role_exist(role)

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
    password = models.CharField(max_length=128)
    firstname = models.CharField(max_length=150, unique=True)
    lastname = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, null=True)
    role = models.CharField(max_length=150, choices=ROLES, default=ROLES[1][1])
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True, unique=False)

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
        if self.role not in ROLES[1]:
            self.group = None

        if self.phone:
            validate_phone(str(self.phone))

        set_password_exist(self=self, password=self.password)

        super().save(*args, **kwargs)
