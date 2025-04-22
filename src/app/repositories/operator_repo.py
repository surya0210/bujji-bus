from app.repositories.base import BaseRepository
from app.entities.operator_entity import Operator
from sqlalchemy.orm import Session


class OperatorRepository(BaseRepository[Operator]):
    def __init__(self,session:Session):
        super().__init__(session,Operator)


    def get_by_email(self,email:str) ->Operator | None:
        return self.session.query(Operator).filter(Operator.email==email).first()
    
    def get_by_id(self,id:str)->Operator | None:
        return self.session.query(Operator).filter(Operator.id==id).first()