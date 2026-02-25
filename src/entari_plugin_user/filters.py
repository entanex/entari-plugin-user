from typing import TypeAlias
from arclet.letoderea import Propagator, STOP, enter_if

from .i18n import Lang
from .annotated import UserSession


class Authorization(Propagator):
    def __init__(self, authority: int, priority: int = 90):
        self.success = True
        self.authority = authority
        self.priority = priority

    async def before(self, session: UserSession):
        self.success = session.user.authority >= self.authority
        if not self.success:
            await session.send(Lang.authority.low_authority())
            return STOP

    async def after(self):
        return

    def compose(self):
        yield self.before, True, self.priority
        yield self.after, False, self.priority


def permission_check(sess: UserSession) -> bool:
    return sess.user.authority == 5


Auth: TypeAlias = Authorization

only_superuser = enter_if(permission_check)
