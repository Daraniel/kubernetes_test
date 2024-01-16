import logging
from typing import List, Union

from sqlalchemy import (Boolean, Column, Float, ForeignKey, Integer, MetaData,
                        String, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (Mapped, backref, mapped_column, relationship,
                            sessionmaker)
from utils.constants import DATABASE

logger = logging.getLogger(__name__)
Base = declarative_base()


class UserTable(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    def __repr__(self):
        return (
            f"<User(username='{self.username}', full_name='{self.full_name}',"
            f" email='{self.email}', disabled={self.disabled}), is_admin={self.is_admin}>"
        )


class InventoryItemTable(Base):
    __tablename__ = "inventory_items"

    item_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    owner: Mapped[int] = mapped_column(ForeignKey("users.id"))
    parent = relationship(
        "UserTable", backref=backref("InventoryItemTable", cascade="all,delete")
    )
    description = Column(String, nullable=True)
    price = Column(Float, nullable=True)

    def __repr__(self):
        return (
            f"InventoryItem(item_id='{self.item_id}', name='{self.name}', owner='{self.owner}',"
            f" description='{self.description}', price={self.price})"
        )


class DatabaseManager:
    def __init__(self, database_name=DATABASE):
        self.engine = create_engine(
            f"sqlite:///{database_name}", echo=False, logging_name=logger.name
        )
        self.metadata = MetaData()
        self.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

        # Create the default user if it doesn't exist, password = secret
        if not self.user_exists("johndoe"):
            self.create_user(
                username="johndoe",
                full_name="John Doe",
                email="johndoe@example.com",
                hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
                is_admin=True,
            )

        # Create the default items if they don't exist
        if not self.get_item_by_name("Item 1"):
            self.create_item(
                name="Item 1", owner=1, description="Description 1", price=10.0
            )
        if not self.get_item_by_name("Item 2"):
            self.create_item(
                name="Item 2", owner=1, description="Description 2", price=20.0
            )

    def create_user(
        self,
        username,
        full_name,
        email,
        hashed_password,
        disabled=False,
        is_admin=False,
    ):
        with self.Session() as session:
            user = UserTable(
                username=username,
                full_name=full_name,
                email=email,
                hashed_password=hashed_password,
                disabled=disabled,
                is_admin=is_admin,
            )

            session.add(user)
            session.commit()

    @staticmethod
    def _get_user_by_username(username, session):
        return session.query(UserTable).filter(UserTable.username == username).first()

    def get_user_by_username(self, username) -> Union[UserTable, None]:
        with self.Session() as session:
            return self._get_user_by_username(username, session)

    def get_all_users(self) -> List[UserTable]:
        with self.Session() as session:
            return session.query(UserTable).all()

    def user_exists(self, username) -> bool:
        with self.Session() as session:
            user = self._get_user_by_username(username, session=session)
            return user is not None

    def remove_user(self, username: str):
        with self.Session() as session:
            user = self._get_user_by_username(username, session=session)
            if user:
                session.delete(user)
                session.commit()
                return True
        return False

    def disable_user(self, username: str):
        with self.Session() as session:
            user = self._get_user_by_username(username, session=session)
            if user:
                user.disabled = True
                session.commit()
                return True
        return False

    def enable_user(self, username: str):
        with self.Session() as session:
            user = self._get_user_by_username(username, session=session)
            if user:
                user.disabled = False
                session.commit()
                return True
        return False

    def make_user_admin(self, username: str):
        with self.Session() as session:
            user = self._get_user_by_username(username, session=session)
            if user:
                user.is_admin = True
                session.commit()
                return True
        return False

    def remove_user_admin(self, username: str):
        with self.Session() as session:
            user = self._get_user_by_username(username, session=session)
            if user:
                user.is_admin = False
                session.commit()
                return True
        return False

    def create_item(
        self, name: str, owner: int, description: str = None, price: float = None
    ):
        item = InventoryItemTable(
            name=name, owner=owner, description=description, price=price
        )
        with self.Session() as session:
            session.add(item)
            session.commit()

    def get_item_by_name(self, name: str) -> Union[InventoryItemTable, None]:
        with self.Session() as session:
            return (
                session.query(InventoryItemTable)
                .filter(InventoryItemTable.name == name)
                .first()
            )

    def get_items_by_owner(self, owner: int) -> List[InventoryItemTable]:
        with self.Session() as session:
            return (
                session.query(InventoryItemTable)
                .filter(InventoryItemTable.owner == owner)
                .all()
            )

    def delete_item(self, name: str):
        with self.Session() as session:
            item = (
                session.query(InventoryItemTable)
                .filter(InventoryItemTable.name == name)
                .first()
            )
            if item:
                session.delete(item)
                session.commit()

    def item_exists(self, name) -> bool:
        item = self.get_item_by_name(name)
        return item is not None


def get_db():
    return DatabaseManager()
