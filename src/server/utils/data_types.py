from typing import Union

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = False
    is_admin: Union[bool, None] = False

    class ConfigDict:
        from_attributes = True


class UserInDB(User):
    id: int
    hashed_password: str

    class ConfigDict:
        from_attributes = True


class InventoryItem(BaseModel):
    name: str
    description: Union[str, None] = None
    price: Union[float, None] = None

    class ConfigDict:
        from_attributes = True


class InventoryItemInDB(InventoryItem):
    item_id: int
    owner: int

    class ConfigDict:
        from_attributes = True
