from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_code = models.CharField(max_length=30, unique=True)
    role_name = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'roles'
        ordering = ['role_id']

    def __str__(self):
        return f'{self.role_code} ({self.role_name})'


class Branch(models.Model):
    branch_id = models.AutoField(primary_key=True)
    ifsc_code = models.CharField(max_length=11, unique=True)
    branch_name = models.CharField(max_length=100)
    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=60, db_index=True)
    state = models.CharField(max_length=60)
    pincode = models.CharField(max_length=6)
    contact_phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'branches'
        ordering = ['branch_id']

    def __str__(self):
        return f'{self.ifsc_code} - {self.branch_name}'


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Username is required')
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)

        role = extra_fields.pop('role', None)
        if role is None:
            role, _ = Role.objects.get_or_create(
                role_code='CUSTOMER',
                defaults={
                    'role_name': 'Retail / Corporate Customer',
                    'description': 'Standard net banking access',
                },
            )

        user = self.model(username=username, email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        admin_role, _ = Role.objects.get_or_create(
            role_code='ADMIN',
            defaults={
                'role_name': 'System Administrator',
                'description': 'Full system configuration and compliance oversight',
            },
        )
        extra_fields.setdefault('role', admin_role)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('kyc_status', 'VERIFIED')
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    KYC_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUBMITTED', 'Submitted'),
        ('VERIFIED', 'Verified'),
        ('REJECTED', 'Rejected'),
    ]

    user_id = models.AutoField(primary_key=True)
    role = models.ForeignKey(Role, on_delete=models.RESTRICT, related_name='users')
    home_branch = models.ForeignKey(
        Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='users'
    )
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=120, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=255, db_column='password_hash')
    full_name = models.CharField(max_length=120, db_index=True)
    date_of_birth = models.DateField(null=True, blank=True)
    pan_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    aadhaar_last4 = models.CharField(max_length=4, null=True, blank=True)
    address_line = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=60, null=True, blank=True)
    state = models.CharField(max_length=60, null=True, blank=True)
    pincode = models.CharField(max_length=6, null=True, blank=True)
    kyc_status = models.CharField(max_length=12, choices=KYC_CHOICES, default='PENDING', db_index=True)
    is_active = models.BooleanField(default=True)
    is_locked = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    failed_login_attempts = models.IntegerField(default=0)
    last_login = models.DateTimeField(null=True, blank=True, db_column='last_login_at')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number', 'full_name']

    class Meta:
        db_table = 'users'
        ordering = ['user_id']

    def __str__(self):
        return f'{self.username} ({self.role.role_code})'
