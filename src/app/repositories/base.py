from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.orm import Session

T = TypeVar("T")
    

class BaseRepository(Generic[T]):
    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model

    def get(self, id: int) -> Optional[T]:
        return self.session.get(self.model, id)

    def list(self) -> List[T]:
        return self.session.query(self.model).all()

    def add(self, obj: T):
        self.session.add(obj)

    def delete(self, obj: T):
        self.session.delete(obj)
