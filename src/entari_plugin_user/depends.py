from arclet.entari import Session, BaseEvent
from entari_plugin_database import get_session

from .models import User, UserSession
from .utils import _get_user, create_user


async def get_user(session: Session[BaseEvent]) -> User:
    async with get_session() as db_session:
        user = await _get_user(
            db_session,
            session.account.platform,
            session.user.id,
        )

        if user is None:
            user = await create_user(session.account.platform, session.user)
            user = await db_session.merge(user)

        return user


async def get_user_session(session: Session[BaseEvent]) -> UserSession[BaseEvent]:
    user = await get_user(session)
    return UserSession(session=session, user=user)
