from unittest.mock import AsyncMock, MagicMock

import pytest
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate
from app.services.user_service import UserService, get_user_service

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
def fake_db():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def user_service(mock_repo) -> UserService:
    return get_user_service(repo=mock_repo)


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
    user_service, mock_repo, fake_db, given_username, given_password, expected_username
):
    given_user = UserCreate(username=given_username, password=given_password)

    mock_repo.create.return_value = User(
        username=given_username, password="hashedpassword"
    )

    user = await user_service.create_user(db=fake_db, data=given_user)

    assert user.username == expected_username
    assert user.password != given_password
    mock_repo.create.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "given_username, given_password, expected_exception",
    [
        ("testuser", "securepassword", IntegrityError),
    ],
)
async def test_create_user_unhappypath(
    user_service, mock_repo, fake_db, given_username, given_password, expected_exception
):
    given_user = UserCreate(username=given_username, password=given_password)

    mock_repo.create.side_effect = IntegrityError("duplicate key", None, None)

    with pytest.raises(expected_exception):
        await user_service.create_user(db=fake_db, data=given_user)


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
    user_service,
    mock_repo,
    fake_db,
    given_username,
    given_password,
    expected_authenticated,
):
    pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

    mock_repo.get_by_username.return_value = User(
        username="testuser", password=pwd.hash("securepassword")
    )

    user = await user_service.authenticate(
        db=fake_db, username=given_username, password=given_password
    )

    if expected_authenticated:
        assert user is not None
        assert user.username == given_username
    else:
        assert user is None
