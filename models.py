from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class RecipeOrm(Base):
    __tablename__ = 'recipes'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    cook_time: Mapped[int] = mapped_column(nullable=False)
    ingredients: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    views: Mapped[int] = mapped_column(default=0)
