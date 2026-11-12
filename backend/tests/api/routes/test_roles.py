from fastapi.testclient import TestClient
from sqlmodel import Session

from app import crud
from app.core.config import settings
from app.models import User, UserCreate, UserRole, UserUpdate
from tests.utils.user import user_authentication_headers
from tests.utils.utils import random_email, random_lower_string


def create_role_user(client: TestClient, db: Session, role: UserRole) -> dict[str, str]:
    email = random_email()
    password = random_lower_string()
    crud.create_user(
        session=db,
        user_create=UserCreate(email=email, password=password, role=role),
    )
    return user_authentication_headers(client=client, email=email, password=password)


def test_manager_can_view_users_but_cannot_change_access(
    client: TestClient, db: Session
) -> None:
    manager_headers = create_role_user(client, db, UserRole.MANAGER)
    response = client.get(f"{settings.API_V1_STR}/users/", headers=manager_headers)
    assert response.status_code == 200

    member = crud.create_user(
        session=db,
        user_create=UserCreate(
            email=random_email(), password=random_lower_string(), role=UserRole.MEMBER
        ),
    )
    response = client.patch(
        f"{settings.API_V1_STR}/users/{member.id}",
        headers=manager_headers,
        json={"role": "admin"},
    )
    assert response.status_code == 403


def test_member_cannot_view_other_users_or_metrics(
    client: TestClient, db: Session
) -> None:
    member_headers = create_role_user(client, db, UserRole.MEMBER)
    assert client.get(f"{settings.API_V1_STR}/users/", headers=member_headers).status_code == 403
    assert client.get(f"{settings.API_V1_STR}/metrics/", headers=member_headers).status_code == 403


def test_role_change_applies_to_existing_session(
    client: TestClient, db: Session
) -> None:
    manager_headers = create_role_user(client, db, UserRole.MANAGER)
    response = client.get(f"{settings.API_V1_STR}/metrics/", headers=manager_headers)
    assert response.status_code == 200

    token_user = client.get(f"{settings.API_V1_STR}/users/me", headers=manager_headers).json()
    user = db.get(User, token_user["id"])
    assert user is not None
    crud.update_user(session=db, db_user=user, user_in=UserUpdate(role=UserRole.MEMBER))
    assert client.get(f"{settings.API_V1_STR}/metrics/", headers=manager_headers).status_code == 403
