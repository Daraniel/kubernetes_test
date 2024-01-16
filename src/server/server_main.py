from utils.logger import setup_logging

# default logging configuration file, used if logging environment variable is not set and/or Uvicorn  logging is not set
default_log_configuration = "./configs/log_conf.yaml"
setup_logging(default_log_configuration)

import logging
from typing import List

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi_responses import custom_openapi
from sqlalchemy.exc import DatabaseError
from typing_extensions import Annotated
from utils.data_types import InventoryItem, Token, User
from utils.database_manager import DatabaseManager, get_db
from utils.user_manager import (get_current_active_user, get_password_hash,
                                get_user_access_token)

logger = logging.getLogger(__name__)
app = FastAPI(
    title="Kubernetes Test",
    description="Test server with FastAPI that has user management system and user inventory",
    version="1.0",
)

# Use auto error api generator provided by fastapi_responses.
# Because of this tool, all error codes are typed as number (rather than using their const object) and the api side code
# is written in the main function of the respective endpoint (it doesn't index errors written in other functions).
app.openapi = custom_openapi(app)


def database_error_handler(_: Request, exc: DatabaseError):
    # Lazily return the error messages created by the DatabaseManager to the user,
    # this is just a test program not a perfect app!
    return JSONResponse(
        status_code=422,
        content={"error": exc.__class__.__name__, "message": exc.args[0]},
    )


app.add_exception_handler(DatabaseError, database_error_handler)


@app.post("/token", response_model=Token)
async def login_for_access_token(
    access_token: Annotated[str, Depends(get_user_access_token)]
):
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/user/users/me/", response_model=User)
async def get_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@app.get("/admin/users/add_user/")
async def add_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
    username: str,
    full_name: str,
    email: str,
    password: str,
    disabled: bool = False,
    is_admin: bool = False,
    db: DatabaseManager = Depends(get_db),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=401, detail="Only admin users can create new users."
        )
    db.create_user(
        username, full_name, email, get_password_hash(password), disabled, is_admin
    )

    return 200


@app.get("/admin/users/get_all_users/", response_model=List[User])
async def get_all_users(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: DatabaseManager = Depends(get_db),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=401, detail="Only admin users can see other users."
        )
    return db.get_all_users()


@app.get("/admin/users/delete_user/")
async def delete_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
    username: str,
    db: DatabaseManager = Depends(get_db),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=401, detail="Only admin users can remove users."
        )
    db.remove_user(username)
    return 200


@app.get("/admin/users/deactivate_user/")
async def deactivate_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
    username: str,
    db: DatabaseManager = Depends(get_db),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=401, detail="Only admin users can disable users."
        )
    db.disable_user(username)
    return 200


@app.get("/admin/users/activate_user/")
async def activate_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
    username: str,
    db: DatabaseManager = Depends(get_db),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=401, detail="Only admin users can enable users."
        )
    db.enable_user(username)
    return 200


@app.get("/admin/users/promote_user/")
async def promote_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
    username: str,
    db: DatabaseManager = Depends(get_db),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=401, detail="Only admin users can make users admin."
        )
    db.make_user_admin(username)
    return 200


@app.get("/admin/users/demote_user/")
async def demote_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
    username: str,
    db: DatabaseManager = Depends(get_db),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=401, detail="Only admin users can make users admin."
        )
    db.remove_user_admin(username)
    return 200


@app.get("/user/items/add_own_item/")
async def add_own_item(
    current_user: Annotated[User, Depends(get_current_active_user)],
    item_name: str,
    description: str = None,
    price: float = None,
    db: DatabaseManager = Depends(get_db),
):
    db.create_item(
        name=item_name, owner=current_user.id, description=description, price=price
    )
    return 200


@app.get("/admin/items/add_item/")
async def add_item(
    current_user: Annotated[User, Depends(get_current_active_user)],
    item_name: str,
    user_name: str,
    description: str = None,
    price: float = None,
    db: DatabaseManager = Depends(get_db),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=401, detail="Only admin users can create item for another user."
        )
    user = db.get_user_by_username(user_name)
    if user is None:
        raise HTTPException(status_code=403, detail="User name not found.")
    db.create_item(name=item_name, owner=user.id, description=description, price=price)
    return 200


@app.get("/user/items/delete_own_item/")
async def delete_own_item(
    current_user: Annotated[User, Depends(get_current_active_user)],
    item_name: str,
    db: DatabaseManager = Depends(get_db),
):
    item = db.get_item_by_name(item_name)
    if item.owner == current_user.id:
        db.delete_item(item_name)
    else:
        raise HTTPException(status_code=401, detail="Item doesn't belong to the user.")
    return 200


@app.get("/admin/items/delete_item/")
async def delete_item(
    current_user: Annotated[User, Depends(get_current_active_user)],
    item_name: str,
    db: DatabaseManager = Depends(get_db),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=200, detail="Only admin users can delete other user's items."
        )
    db.delete_item(name=item_name)
    return 200


@app.get("/user/items/get_own_item_by_name/", response_model=InventoryItem)
async def get_own_item_by_name(
    current_user: Annotated[User, Depends(get_current_active_user)],
    item_name: str,
    db: DatabaseManager = Depends(get_db),
):
    item = db.get_item_by_name(item_name)
    if item.owner == current_user.id:
        return item
    else:
        raise HTTPException(status_code=401, detail="Item doesn't belong to the user.")


@app.get("/admin/items/get_item_by_name/", response_model=InventoryItem)
async def get_item_by_name(
    current_user: Annotated[User, Depends(get_current_active_user)],
    item_name: str,
    db: DatabaseManager = Depends(get_db),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=401, detail="Only admin users can see other user's items."
        )
    return db.get_item_by_name(item_name)


@app.get("/user/items/get_own_items/", response_model=List[InventoryItem])
async def get_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: DatabaseManager = Depends(get_db),
):
    return [
        InventoryItem(**item.__dict__)
        for item in db.get_items_by_owner(current_user.id)
    ]


@app.get("/admin/items/get_items/", response_model=List[InventoryItem])
async def get_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
    user_name: str,
    db: DatabaseManager = Depends(get_db),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=401, detail="Only admin users get other user's items."
        )
    user = db.get_user_by_username(user_name)
    if user is None:
        raise HTTPException(status_code=403, detail="User name not found.")
    return [InventoryItem(**item.__dict__) for item in db.get_items_by_owner(user.id)]


@app.get("/")
def read_main(request: Request):
    # return something when accessing the root directory, can be useful for debugging
    return {
        "message": "Hello World",
        "root_path": request.scope.get("root_path"),
        "docs_path": request.scope.get("root_path") + "/docs",
    }


if __name__ == "__main__":
    # access the docs at http://127.0.0.1:8000/docs
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=default_log_configuration)
