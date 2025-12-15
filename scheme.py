from pydantic import BaseModel, ValidationError
from errors import HttpError

class BaseAnnouncement(BaseModel):
    title: str
    discription: str
    owner:str
    
class CreateAnnouncement(BaseAnnouncement):
    pass
    
class UpdateAnnouncement(BaseModel):
    title: str | None = None
    discription: str | None = None
    owner: str | None = None
    
def validate(json_data: dict, scheme_cls: type[CreateAnnouncement | UpdateAnnouncement]):
    try:
        ancmnt_scheme = scheme_cls(**json_data)
        return ancmnt_scheme.model_dump(exclude_none=True)
    except ValidationError as er:
        errs = er.errors()
        for err in errs:
            err.pop("ctx", None)
        raise HttpError(400, errs)