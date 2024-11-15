from Data.models import Moderators, Base, Customers
from sqlalchemy import select, delete, update

from Data.db import sync_engine, async_session

def create_tables():
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)

class Core:

    @staticmethod
    async def GetAllModerators():
        async with async_session() as session:
            res = await session.execute(select(Moderators))
            queryset = res.scalars().all()
            queryset = [(m.nickname, m.pk) for m in queryset]
            return queryset

    @staticmethod
    async def GetAllModeratorsView():
        async with async_session() as session:
            res = await session.execute(select(Moderators))
            queryset = res.scalars().all()
            queryset = [m.nickname for m in queryset]
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

    @staticmethod
    async def GetAllClients():
        async with async_session() as session:
            res = await session.execute(select(Customers))
            queryset = res.scalars().all()
            queryset = [(c.name, c.surname, c.number, c.bonuses, c.pk) for c in queryset]
            return queryset

    @staticmethod
    async def DeleteClient(pk, number):
        async with async_session() as session:
            await session.execute(delete(Customers).where(
                Customers.pk == pk,
                Customers.number == number
            ))
            await session.commit()

    @staticmethod
    async def IncreaseBonuses(number, value):
        async with async_session() as session:
            
            await session.execute(
                update(Customers)
                .where(
                    Customers.number == number)
                .values(
                    bonuses = Customers.bonuses + value
                )
            )
            await session.commit()

    @staticmethod
    async def DecreaseBonuses(number, value):
        async with async_session() as session:

            obj = await session.execute(select(Customers).where(Customers.number == number))
            user = obj.scalar()

            if user.bonuses <= value:
                await session.execute(
                    update(Customers)
                    .where(
                        Customers.number == number)
                    .values(
                        bonuses = 0
                    )
                )
            else:
                await session.execute(
                    update(Customers)
                    .where(
                        Customers.number == number)
                    .values(
                        bonuses = Customers.bonuses - value
                    )
                )
            await session.commit()

    @staticmethod
    async def CreateClient(name, surname, number):
        async with async_session() as session:
            user = Customers(name=name, surname=surname, number=str(number))
            session.add(user)
            await session.commit()

    @staticmethod
    async def FindClient(number, statement):
        async with async_session() as session:
            if statement == 'NUMBER':
                res = await session.execute(select(Customers).where(Customers.number == str(number)))
            else:
                res = await session.execute(select(Customers).where(Customers.pk == number))
            user = res.scalar()

            if user is None:
                return False 
            else:
                return (user.name, user.surname, user.number, user.bonuses)
            
    @staticmethod
    async def ChangeNumber(pk, number):
        async with async_session() as session:
            await session.execute(
                update(Customers)
                    .where(
                        Customers.pk == pk
                    )
                    .values(
                        number = number
                    )
            )
            await session.commit()