from unittest.mock import AsyncMock, MagicMock

import pytest
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.schemas.user import UserCreate
from app.services.user_service import UserService

# -----------------------------
# Fixtures
# -----------------------------


@pytest.fixture
def mock_repo():
    repo = MagicMock()
    repo.get_by_username = AsyncMock()
    repo.create = AsyncMock()
    return repo


@pytest.fixture
def user_service(mock_repo) -> UserService:
    return UserService(repo=mock_repo)


# -----------------------------
# Tests
# -----------------------------


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "given_username, given_password, expected_username",
    [
        ("testuser", "securepassword", "testuser"),
        ("alice", "password123", "alice"),
    ],
)
async def test_create_user_happypath(
    user_service, mock_repo, given_username, given_password, expected_username
):
    given_user = UserCreate(username=given_username, password=given_password)

    mock_repo.create.return_value = User(
        username=given_username, password="hashedpassword"
    )

    user = await user_service.create_user(data=given_user)

    assert user.username == expected_username
    assert user.password != given_password

    mock_repo.create.assert_awaited_once()
    called_user = mock_repo.create.call_args.kwargs["user"]
    assert called_user.username == given_username
    assert called_user.password != given_password


@pytest.mark.asyncio
async def test_create_user_unhappypath(user_service, mock_repo):
    given_user = UserCreate(username="testuser", password="securepassword")

    mock_repo.create.side_effect = IntegrityError("duplicate key", None, None)

    import pytest

    with pytest.raises(IntegrityError):
        await user_service.create_user(data=given_user)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "given_username, given_password, expected_authenticated",
    [
        ("testuser", "securepassword", True),
        ("testuser", "wrongpassword", False),
        ("nonexistent", "any", False),
    ],
)
async def test_authenticate(
    user_service, mock_repo, given_username, given_password, expected_authenticated
):
    pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def get_by_username_side_effect(username):
        if username == "testuser":
            return User(username="testuser", password=pwd.hash("securepassword"))
        return None

    mock_repo.get_by_username.side_effect = get_by_username_side_effect

    user = await user_service.authenticate(
        username=given_username, password=given_password
    )

    if expected_authenticated:
        assert user is not None
        assert user.username == given_username
    else:
        assert user is None
