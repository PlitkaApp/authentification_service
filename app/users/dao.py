from app.dao import BaseDAO
from app.users.models import User

class UsersDAO(BaseDAO):
    model = User

    @classmethod
    async def get_user_roles(cls, user_id: int) -> list[str]:
        user = await cls.find_one_or_none(id = user_id)
        role_mapping = ['user', 'premium', 'tester', 'admin', 'content_manager', 'system_analyst']

        return [
            role_name
            for role_name in role_mapping
            if getattr(user, role_name, False)
        ]

    @classmethod
    async def update_roles(cls, user_id: int, new_roles: list[str]):
        update_roles = {
            'user': False,
            'premium': False,
            'tester': False,
            'admin': False,
            'content_manager': False,
            'system_analyst': False
        }
        for role in new_roles:
            update_roles[f'{role}'] = True
        check = await cls.update({'id': user_id}, **update_roles)
        return check