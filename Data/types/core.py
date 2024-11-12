from Data.models import Moderators, Base
from sqlalchemy import select, delete

from Data.db import sync_engine, async_session

def create_tables():
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)

class Core:

    @staticmethod
    async def AddUser(tg_id, nickname):
        async with async_session() as session:
            user = Moderators(nickname=nickname, tg_id=tg_id)
            session.add(user)
            await session.commit()

    @staticmethod
    async def GetAllModerators():
        async with async_session() as session:
            res = await session.execute(select(Moderators))
            queryset = res.scalars().all()
            queryset = [(u.nickname, u.pk) for u in queryset]
            return queryset
        
    @staticmethod
    async def DeleteModerator(pk, nickname):
        async with async_session() as session:
            await session.execute(delete(Moderators).where(
                Moderators.nickname == nickname,
                Moderators.pk == pk
                    )
                )
            await session.commit()
        
    @staticmethod
    async def CreateModerator(nickname):
        async with async_session() as session:
            moderator = Moderators(nickname=nickname)
            session.add(moderator)
            await session.commit()
