# app/todos/crud.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.todo import models, schemas

# جلب كل المهام
async def get_todos(db: AsyncSession):
    result = await db.execute(select(models.Todo))
    return result.scalars().all()

# جلب مهمة واحدة بالـ ID
async def get_todo(db: AsyncSession, todo_id: int):
    result = await db.execute(
        select(models.Todo).where(models.Todo.id == todo_id)
    )
    return result.scalar_one_or_none()

# إنشاء مهمة جديدة
async def create_todo(db: AsyncSession, todo: schemas.TodoCreate, user_id: int):
    db_todo = models.Todo(**todo.dict(), user_id=user_id)
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo
