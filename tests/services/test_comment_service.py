from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.models.comment import Comment
from app.schemas.comment import CommentCreate
from app.services.comment_service import CommentService


@pytest.fixture
def mock_repo():
    repo = MagicMock()
    repo.create = AsyncMock()
    repo.list_by_post = AsyncMock()
    return repo


@pytest.fixture
def comment_service(mock_repo):
    return CommentService(repo=mock_repo)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "content, post_id, user_id",
    [
        ("Nice post!", 1, 42),
        ("Great article", 2, 7),
        ("Thanks for sharing", 3, 13),
    ],
)
async def test_create_comment(comment_service, mock_repo, content, post_id, user_id):
    data = CommentCreate(content=content, post_id=post_id)

    with patch(
        "app.services.comment_service.Comment", new_callable=MagicMock
    ) as mock_comment:
        mock_instance = mock_comment.return_value
        mock_repo.create.return_value = mock_instance

        comment = await comment_service.create_comment(data=data, user_id=user_id)

        mock_repo.create.assert_awaited_once_with(comment=mock_instance)
        mock_comment.assert_called_once_with(
            content=content, post_id=post_id, user_id=user_id
        )
        assert comment == mock_instance


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "post_id, expected_comments",
    [
        (1, [MagicMock(spec=Comment), MagicMock(spec=Comment)]),
        (2, [MagicMock(spec=Comment)]),
        (3, []),
    ],
)
async def test_list_comments(comment_service, mock_repo, post_id, expected_comments):
    mock_repo.list_by_post = AsyncMock(return_value=expected_comments)

    result = await comment_service.list_comments(post_id=post_id)

    mock_repo.list_by_post.assert_awaited_once_with(post_id)
    assert result == expected_comments
