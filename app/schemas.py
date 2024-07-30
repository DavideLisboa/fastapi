from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str
    completed: bool = False


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class TaskPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True
