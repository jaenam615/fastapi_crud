from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models.post import Post
from app.schemas.post import PostCreate
from app.services.post_service import PostService

# -----------------------------
# Fixtures
# -----------------------------


@pytest.fixture
def mock_repo():
    repo = MagicMock()
    repo.create = AsyncMock()
    repo.list = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.delete = AsyncMock()
    return repo


@pytest.fixture
def post_service(mock_repo) -> PostService:
    return PostService(repo=mock_repo)


# -----------------------------
# Tests
# -----------------------------


@pytest.mark.asyncio
async def test_create_post(post_service, mock_repo):
    data = PostCreate(title="Hello", content="World")
    mock_repo.create.return_value = Post(title="Hello", content="World", user_id=1)

    post = await post_service.create_post(data=data, user_id=1)

    assert post.title == "Hello"
    assert post.content == "World"
    assert post.user_id == 1

    mock_repo.create.assert_awaited_once()
    called_post = mock_repo.create.call_args.kwargs["post"]
    assert called_post.title == "Hello"
    assert called_post.content == "World"
    assert called_post.user_id == 1


@pytest.mark.asyncio
async def test_list_posts(post_service, mock_repo):
    posts = [
        Post(title="A", content="AAA", user_id=1),
        Post(title="B", content="BBB", user_id=2),
    ]
    mock_repo.list.return_value = posts

    result = await post_service.list_posts()

    assert result == posts
    mock_repo.list.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_post_by_id(post_service, mock_repo):
    mock_repo.get_by_id.return_value = Post(title="X", content="Y", user_id=1)

    post = await post_service.get_post_by_id(post_id=42)

    assert post.title == "X"
    assert post.content == "Y"
    assert post.user_id == 1
    mock_repo.get_by_id.assert_awaited_once_with(post_id=42)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "post_user_id, user_id, expected_result",
    [
        (1, 1, True),
        (1, 2, False),
        (None, 1, False),
    ],
)
async def test_delete_post(
    post_service, mock_repo, post_user_id, user_id, expected_result
):
    if post_user_id is None:
        mock_repo.get_by_id.return_value = None
    else:
        mock_repo.get_by_id.return_value = Post(
            title="X", content="Y", user_id=post_user_id
        )

    result = await post_service.delete_post(user_id=user_id, post_id=10)

    assert result == expected_result
    mock_repo.get_by_id.assert_awaited_once_with(post_id=10)
    if expected_result:
        mock_repo.delete.assert_awaited_once_with(post_id=10)
    else:
        mock_repo.delete.assert_not_awaited()
