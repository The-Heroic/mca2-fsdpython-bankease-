from django.contrib.auth import password_validation
from django.db.models import Q
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import Branch, Role, User


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['branch_id', 'ifsc_code', 'branch_name', 'city', 'state', 'pincode']


class UserProfileSerializer(serializers.ModelSerializer):
    role_code = serializers.CharField(source='role.role_code', read_only=True)
    role_name = serializers.CharField(source='role.role_name', read_only=True)
    branch_ifsc = serializers.CharField(source='home_branch.ifsc_code', read_only=True, default=None)
    branch_name = serializers.CharField(source='home_branch.branch_name', read_only=True, default=None)

    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'email',
            'phone_number',
            'full_name',
            'role_code',
            'role_name',
            'branch_ifsc',
            'branch_name',
            'kyc_status',
            'is_active',
            'is_locked',
            'last_login',
            'created_at',
        ]
        read_only_fields = fields


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'phone_number',
            'full_name',
            'password',
            'confirm_password',
            'city',
            'state',
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password': 'Passwords do not match.'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        customer_role, _ = Role.objects.get_or_create(
            role_code='CUSTOMER',
            defaults={
                'role_name': 'Retail / Corporate Customer',
                'description': 'Standard net banking access',
            },
        )
        return User.objects.create_user(
            role=customer_role,
            password=password,
            **validated_data,
        )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username', '').strip()
        password = attrs.get('password', '')

        user_obj = User.objects.select_related('role', 'home_branch').filter(
            Q(username__iexact=username) | Q(email__iexact=username)
        ).first()

        if not user_obj:
            raise serializers.ValidationError({'detail': 'Invalid username or password.'})

        if user_obj.is_locked or not user_obj.is_active:
            raise serializers.ValidationError(
                {'detail': 'Account is locked or inactive. Please contact BankEase support.'}
            )

        if not user_obj.check_password(password):
            user_obj.failed_login_attempts += 1
            if user_obj.failed_login_attempts >= 3:
                user_obj.is_locked = True
            user_obj.save(update_fields=['failed_login_attempts', 'is_locked'])
            raise serializers.ValidationError({'detail': 'Invalid username or password.'})

        user = user_obj
        user.failed_login_attempts = 0
        user.last_login = timezone.now()
        user.save(update_fields=['failed_login_attempts', 'last_login'])

        refresh = RefreshToken.for_user(user)
        refresh['role'] = user.role.role_code if user.role else 'CUSTOMER'
        refresh['username'] = user.username

        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserProfileSerializer(user).data,
        }


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.check_password(attrs['current_password']):
            raise serializers.ValidationError({'current_password': 'Current password is incorrect.'})
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError({'confirm_new_password': 'New passwords do not match.'})
        password_validation.validate_password(attrs['new_password'], user=user)
        return attrs
