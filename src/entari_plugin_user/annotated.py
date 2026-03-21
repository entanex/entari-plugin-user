from typing import Annotated

from arclet.letoderea import Depends

from .models import E
from .models import User as _User
from .models import UserSession as _UserSession
from .depends import get_user, get_user_session

User = Annotated[_User, Depends(get_user)]
UserSession = Annotated[_UserSession[E], Depends(get_user_session)]
