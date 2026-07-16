from pydantic import BaseModel, ConfigDict


class BaseRecipe(BaseModel):
    name: str
    cook_time: int


class RecipeIn(BaseRecipe):
    ingredients: str
    description: str


class RecipeOut(BaseRecipe):
    id: int
    views: int
    ingredients: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class RecipeSummaryOut(BaseRecipe):
    views: int

    model_config = ConfigDict(from_attributes=True)
