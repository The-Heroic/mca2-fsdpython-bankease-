import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts_auth.models import Role, User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def customer_role(db):
    role, _ = Role.objects.get_or_create(
        role_code='CUSTOMER',
        defaults={
            'role_name': 'Retail / Corporate Customer',
            'description': 'Standard net banking access',
        },
    )
    return role


@pytest.mark.django_db
def test_health_check(api_client):
    response = api_client.get(reverse('health-check'))
    assert response.status_code == status.HTTP_200_OK
    assert response.data['status'] == 'ok'
    assert response.data['service'] == 'BankEase API'


@pytest.mark.django_db
def test_customer_registration_and_login_flow(api_client, customer_role):
    register_payload = {
        'username': 'test_aarav',
        'email': 'test.aarav@bankease.in',
        'phone_number': '+91-9811199999',
        'full_name': 'Aarav Test User',
        'password': 'BankEase@2026',
        'confirm_password': 'BankEase@2026',
        'city': 'Noida',
        'state': 'Uttar Pradesh',
    }
    reg_res = api_client.post(reverse('auth-register'), register_payload, format='json')
    assert reg_res.status_code == status.HTTP_201_CREATED
    assert reg_res.data['user']['role_code'] == 'CUSTOMER'

    login_res = api_client.post(
        reverse('auth-login'),
        {'username': 'test_aarav', 'password': 'BankEase@2026'},
        format='json',
    )
    assert login_res.status_code == status.HTTP_200_OK
    assert 'access' in login_res.data
    assert 'refresh' in login_res.data

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_res.data['access']}")
    me_res = api_client.get(reverse('auth-profile'))
    assert me_res.status_code == status.HTTP_200_OK
    assert me_res.data['username'] == 'test_aarav'


@pytest.mark.django_db
def test_account_locks_after_three_failed_attempts(api_client, customer_role):
    User.objects.create_user(
        username='lock_test_user',
        email='lock@bankease.in',
        phone_number='+91-9811188888',
        full_name='Lock Test User',
        password='CorrectPassword@1',
        role=customer_role,
    )

    for _ in range(3):
        res = api_client.post(
            reverse('auth-login'),
            {'username': 'lock_test_user', 'password': 'WrongPassword'},
            format='json',
        )
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    user = User.objects.get(username='lock_test_user')
    assert user.is_locked is True
    assert user.failed_login_attempts == 3

    # Even with correct password, locked account cannot log in
    locked_res = api_client.post(
        reverse('auth-login'),
        {'username': 'lock_test_user', 'password': 'CorrectPassword@1'},
        format='json',
    )
    assert locked_res.status_code == status.HTTP_400_BAD_REQUEST
