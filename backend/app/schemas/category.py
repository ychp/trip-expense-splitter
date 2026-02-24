from pydantic import BaseModel, Field
from typing import Optional


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="分类名称")
    type: str = Field(..., description="分类类型: income/expense")
    parent_id: Optional[int] = Field(None, description="父分类ID")
    sort_order: int = Field(default=0, ge=0, description="排序顺序")


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    type: Optional[str] = None
    parent_id: Optional[int] = None
    sort_order: Optional[int] = Field(None, ge=0)


class CategoryResponse(CategoryBase):
    id: int
    
    class Config:
        from_attributes = True
