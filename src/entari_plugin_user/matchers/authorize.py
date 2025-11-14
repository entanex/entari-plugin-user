from arclet.alconna import Alconna, CommandMeta, Args, Option
from arclet.entari import command, At

from ..i18n import Lang
from ..annotated import UserSession
from ..filters import Authorization
from ..utils import get_user, set_user_authority

authorize_alc = Alconna(
    "authorize",
    Args["value#权限等级", int],
    Option("-u", Args["user#目标用户", At]),
    meta=CommandMeta(
        description="设置用户的权限等级",
        usage="authorize <value> -u <user>",
        example="authorize 3 -u @miraita",
    ),
)
authorize_alc.shortcut("auth", {"command": "authorize", "fuzzy": True, "prefix": True})
authorize_disp = command.mount(authorize_alc)


@authorize_disp.handle()
async def authorize_(value: int, user: At, session: UserSession):
    if user.id is None:
        return

    operator_user = session.user
    target_user = await get_user(session.platform, user.id)

    if target_user.authority >= operator_user.authority:
        await session.session.send(Lang.authority.low_authority())
        return

    if value >= operator_user.authority:
        await session.session.send(Lang.authority.low_authority())
        return

    await set_user_authority(session.user_id, value)
    await session.session.send(Lang.authority.success())


authorize_.propagate(Authorization(4))
