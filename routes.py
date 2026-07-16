from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models
import schemas
from database import engine, get_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.post('/recipes', response_model=schemas.RecipeOut)
async def create_recipe(
        recipe: schemas.RecipeIn,
        session: AsyncSession = Depends(get_session)
):
    try:
        new_recipe = models.RecipeOrm(**recipe.model_dump())
        session.add(new_recipe)
        await session.commit()
        await session.refresh(new_recipe)

        return new_recipe
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.get('/recipes', response_model=list[schemas.RecipeSummaryOut])
async def get_recipes(
        session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(models.RecipeOrm)
        .order_by(
            desc(models.RecipeOrm.views),
            asc(models.RecipeOrm.cook_time)
        )
    )
    return result.scalars().all()


@app.get('/recipes/{id_r}', response_model=schemas.RecipeOut)
async def get_recipe(
        id_r: int,
        session: AsyncSession = Depends(get_session)
):
    recipe = await session.get(models.RecipeOrm, id_r)
    if not recipe:
        raise HTTPException(status_code=404, detail='Recipe not found')

    recipe.views += 1
    await session.commit()
    await session.refresh(recipe)

    return recipe
