from typing import List
from src import db


class Apex:
    @property
    def sigma_x(self) -> float:
        return self.__sigma_x

    @sigma_x.setter
class Image(db.Model):  # type: ignore
    id: int = db.Column(db.Integer, primary_key=True)  # type: ignore
    path: str = db.Column(db.String(100), nullable=False)  # type: ignore
    apexes: List[] = db.Column(db.)
