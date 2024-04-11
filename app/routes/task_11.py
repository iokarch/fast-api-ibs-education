from fastapi import APIRouter, Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, UserFromDB
from app.db.database import get_async_session
from app.db.dbmodels import UserTable

router = APIRouter(tags=["SQLAlchemy"])


@router.get("/get_users/", response_model=list[UserFromDB])
async def get_users(session: AsyncSession = Depends(get_async_session)):
    """
    Возвращает всех пользователей
    """
    result = await session.execute(select(UserTable))
    return result.scalars().all()
    

@router.post("/get_user/", response_model=UserFromDB)
async def get_user(id_user: int, session: AsyncSession = Depends(get_async_session)):
    """
    Возвращает пользователя по ID
    """
    result = await session.get(UserTable, id_user)
    print(result)
    return result
    

@router.delete("/delete_user/{id}")
async def delete_user(id_user: int, session: AsyncSession = Depends(get_async_session)):
    """
    Удаляет пользователя по ID
    """
    result = await session.get(UserTable, id_user)
    await session.delete(result)
    await session.commit()
    return "Запись удалена!"


@router.put("/update_user/{id}")
async def update_user(id: int, new_user: User, session: AsyncSession = Depends(get_async_session)):
    """
    Изменяет пользователя по его ID
    """
    result = await session.get(UserTable, id)
    result.name = new_user.name
    result.age = new_user.age
    result.adult = result.age >= 18
    result.message = new_user.message
    await session.commit()
    return result

@router.put("/update_user_name/{id}")
async def update_user_name(id: int, new_name: str, session: AsyncSession = Depends(get_async_session)):
    """
    Изменяет имя сообщения пользователя по его ID
    """
    result = await session.get(UserTable, id)
    result.name = new_name
    await session.commit()
    return result


@router.put("/update_user_age/{id}")
async def update_user_age(id: int, new_age: int, session: AsyncSession = Depends(get_async_session)):
    """
    Изменяет возраст пользователя по его ID
    """
    result = await session.get(UserTable, id)
    result.age = new_age
    result.adult = result.age >= 18
    await session.commit()
    return result


@router.put("/update_user_message/{id}")
async def update_user_message(id: int, new_message: str, session: AsyncSession = Depends(get_async_session)):
    """
    Изменяет строку сообщения пользователя по его ID
    """
    result = await session.get(UserTable, id)
    result.message = new_message
    await session.commit()
    return result


@router.post("/add_user/", response_model=User)
async def create_user(user: UserFromDB, session: AsyncSession = Depends(get_async_session)):
    """
    Создает нового пользователя
    """
    new_user = UserTable(**user.model_dump())
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user
