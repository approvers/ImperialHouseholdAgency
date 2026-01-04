import logfire
from injector import inject

from src.system.domain.interface.repository.common.response import (
    RepositoryResultStatusEnum,
)
from src.system.domain.interface.repository.messenger import MessengerRepository
from src.system.domain.interface.repository.nickname import NicknameChangelogRepository
from src.system.domain.interface.repository.user import UserRepository
from src.system.domain.model.nickname import NicknameChangelog
from src.system.domain.model.user import User
from src.system.domain.value.nickname import (
    NicknameChangelogRecordID,
    NicknameChangelogCreatedAt,
    NicknameChangelogUserRecordID,
)
from src.system.domain.value.user import (
    UserRecordID,
    UserCreatedAt,
    UserUpdatedAt,
    UserMessengerRecordID,
)
from src.system.usecase.nickname.dto import (
    RecordNicknameChangeRequest,
    RecordNicknameChangeResponse,
)
from src.system.usecase.nickname.interface import RecordNicknameChangeUsecaseIf
from src.system.util.datetime import utcnow
from src.system.util.id import generate_ulid


class RecordNicknameChangeUsecase(RecordNicknameChangeUsecaseIf):
    """Usecase for recording nickname changes."""

    @inject
    def __init__(
        self,
        messenger_repository: MessengerRepository,
        user_repository: UserRepository,
        nickname_changelog_repository: NicknameChangelogRepository,
    ) -> None:
        self.messenger_repository = messenger_repository
        self.user_repository = user_repository
        self.nickname_changelog_repository = nickname_changelog_repository

    @logfire.instrument(span_name="RecordNicknameChangeUsecase.execute()")
    async def execute(
        self, request: RecordNicknameChangeRequest
    ) -> RecordNicknameChangeResponse:
        now = utcnow()

        # メッセンジャーを取得
        messenger_response = await self.messenger_repository.get_by_name(
            request.messenger_name
        )

        if messenger_response.is_success == RepositoryResultStatusEnum.ERROR:
            return RecordNicknameChangeResponse(
                is_success=False,
                message=messenger_response.message,
            )

        if messenger_response.response is None:
            return RecordNicknameChangeResponse(
                is_success=False,
                message=f"Messenger not found: {request.messenger_name.root}",
            )

        messenger = messenger_response.response

        # ユーザーを取得または作成
        user = User(
            record_id=UserRecordID(generate_ulid(now)),
            created_at=UserCreatedAt(now),
            updated_at=UserUpdatedAt(now),
            messenger_record_id=UserMessengerRecordID(messenger.record_id.root),
            id=request.user_id,
        )

        user_response = await self.user_repository.get_or_create(user)

        if user_response.is_success == RepositoryResultStatusEnum.ERROR:
            return RecordNicknameChangeResponse(
                is_success=False,
                message=user_response.message,
            )

        if user_response.response is None:
            return RecordNicknameChangeResponse(
                is_success=False,
                message="Failed to get or create user",
            )

        existing_user = user_response.response

        # ニックネーム変更履歴を作成
        nickname_changelog = NicknameChangelog(
            record_id=NicknameChangelogRecordID(generate_ulid(now)),
            created_at=NicknameChangelogCreatedAt(now),
            user_record_id=NicknameChangelogUserRecordID(existing_user.record_id.root),
            before=request.before,
            after=request.after,
        )

        changelog_response = await self.nickname_changelog_repository.create(
            nickname_changelog
        )

        if changelog_response.is_success == RepositoryResultStatusEnum.ERROR:
            return RecordNicknameChangeResponse(
                is_success=False,
                message=changelog_response.message,
            )

        return RecordNicknameChangeResponse(is_success=True)
