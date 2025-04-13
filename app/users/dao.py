from app.dao import BaseDAO
from app.users.models import User

class UsersDAO(BaseDAO):
    model = User

    @classmethod
    async def get_user_roles(cls, user_id: int) -> list[str]:
        user = await cls.find_one_or_none(id = user_id)
        roles = []
        if user.is_user:
            roles.append('user')
        if user.is_premium_user:
            roles.append('premium')
        if user.is_tester:
            roles.append('tester')
        if user.is_admin:
            roles.append('admin')
        if user.is_content_manager:
            roles.append('content_manager')
        if user.is_system_analyst:
            roles.append('system_analyst')
        return roles