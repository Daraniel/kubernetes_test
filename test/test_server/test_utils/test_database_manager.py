import os
import tempfile
import unittest


class TestUserDatabase(unittest.TestCase):
    def setUp(self):
        # Create a temporary database file for testing
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp()
        os.environ["DATABASE"] = self.temp_db_path
        from utils.database_manager import DatabaseManager

        self.db_manager = DatabaseManager(database_name=self.temp_db_path)

    def tearDown(self):
        # Close and remove the temporary database file
        os.close(self.temp_db_fd)
        try:
            os.unlink(self.temp_db_path)
        except Exception:
            pass  # folder sometimes gets auto removed

    def test_create_user(self):
        # Test creating a new user
        self.db_manager.create_user(
            username="testuser",
            full_name="Test UserTable",
            email="testuser@example.com",
            hashed_password="testpassword",
            disabled=True,
            is_admin=True,
        )

        # Test if the user exists
        self.assertTrue(self.db_manager.user_exists("testuser"))

        # Retrieve the user from the database
        user = self.db_manager.get_user_by_username("testuser")

        # Check if the user is not None
        self.assertIsNotNone(user)

        # Check if user attributes match the expected values
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.full_name, "Test UserTable")
        self.assertEqual(user.email, "testuser@example.com")
        self.assertEqual(user.hashed_password, "testpassword")
        self.assertTrue(user.disabled, "testpassword")
        self.assertTrue(user.is_admin, "testpassword")

        self.db_manager.create_user(
            username="testuser2",
            full_name="Test UserTable 2",
            email="testuser2@example.com",
            hashed_password="testpassword2",
        )

        # Retrieve the user from the database
        user = self.db_manager.get_user_by_username("testuser2")

        # Check if the user is not None
        self.assertIsNotNone(user)

        # Check if user attributes match the expected values
        self.assertEqual(user.username, "testuser2")
        self.assertEqual(user.full_name, "Test UserTable 2")
        self.assertEqual(user.email, "testuser2@example.com")
        self.assertEqual(user.hashed_password, "testpassword2")
        self.assertFalse(user.disabled)
        self.assertFalse(user.is_admin)

        self.assertEqual(len(self.db_manager.get_all_users()), 3)

    def test_get_user_by_username(self):
        from utils.database_manager import UserTable

        # Test retrieving an existing user by username
        existing_user = UserTable(
            username="existinguser",
            full_name="Existing UserTable",
            email="existinguser@example.com",
            hashed_password="existingpassword",
        )
        with self.db_manager.Session() as session:
            session.add(existing_user)
            session.commit()

        # Retrieve the user from the database
        user = self.db_manager.get_user_by_username("existinguser")

        # Check if the user is not None
        self.assertIsNotNone(user)

        # Check if user attributes match the expected values
        self.assertEqual(user.username, "existinguser")
        self.assertEqual(user.full_name, "Existing UserTable")
        self.assertEqual(user.email, "existinguser@example.com")
        self.assertEqual(user.hashed_password, "existingpassword")
        self.assertFalse(user.disabled)

    def test_get_user_by_username_nonexistent(self):
        # Test retrieving a non-existent user by username
        user = self.db_manager.get_user_by_username("nonexistentuser")

        # Check if the user is None
        self.assertIsNone(user)

        # Checks if it doesn't exist directly
        self.assertFalse(self.db_manager.user_exists("nonexistentuser"))

    def test_remove_user(self):
        self.db_manager.create_user(
            username="testuser",
            full_name="Test UserTable",
            email="testuser@example.com",
            hashed_password="testpassword",
            disabled=False,
            is_admin=True,
        )

        # Test removing a user
        self.db_manager.remove_user("testuser")
        user = self.db_manager.get_user_by_username("testuser")
        self.assertIsNone(user)

    def test_disable_user(self):
        self.db_manager.create_user(
            username="testuser",
            full_name="Test UserTable",
            email="testuser@example.com",
            hashed_password="testpassword",
            disabled=False,
            is_admin=True,
        )

        # Test disabling a user
        self.db_manager.disable_user("testuser")
        user = self.db_manager.get_user_by_username("testuser")
        self.assertTrue(user.disabled)

    def test_enable_user(self):
        self.db_manager.create_user(
            username="testuser",
            full_name="Test UserTable",
            email="testuser@example.com",
            hashed_password="testpassword",
            disabled=True,
            is_admin=True,
        )

        # Test enabling a user
        self.db_manager.enable_user("testuser")
        user = self.db_manager.get_user_by_username("testuser")
        self.assertFalse(user.disabled)

    def test_make_user_admin(self):
        self.db_manager.create_user(
            username="testuser",
            full_name="Test UserTable",
            email="testuser@example.com",
            hashed_password="testpassword",
            disabled=False,
            is_admin=False,
        )

        # Test making a user an admin
        self.db_manager.make_user_admin("testuser")
        user = self.db_manager.get_user_by_username("testuser")
        self.assertTrue(user.is_admin)

    def test_remove_user_admin(self):
        self.db_manager.create_user(
            username="testuser",
            full_name="Test UserTable",
            email="testuser@example.com",
            hashed_password="testpassword",
            disabled=False,
            is_admin=True,
        )

        # Test removing admin status from a user
        self.db_manager.remove_user_admin("testuser")
        user = self.db_manager.get_user_by_username("testuser")
        self.assertFalse(user.is_admin)


class TestInventoryItemDatabase(unittest.TestCase):
    def setUp(self):
        # Create a temporary database file for testing
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp()
        os.environ["DATABASE"] = self.temp_db_path
        from utils.database_manager import DatabaseManager

        self.db_manager = DatabaseManager(database_name=self.temp_db_path)

    def tearDown(self):
        # Close and remove the temporary database file
        os.close(self.temp_db_fd)
        try:
            os.unlink(self.temp_db_path)
        except Exception:
            pass  # folder sometimes gets auto removed

    def test_create_item(self):
        # Test creating a new item
        self.db_manager.create_item(
            name="Item 10", owner=1, description="Description 1", price=10.0
        )

        # Test if the item exists
        item = self.db_manager.get_item_by_name(name="Item 10")
        self.assertIsNotNone(item)

        # Check if item attributes match the expected values
        self.assertEqual(item.name, "Item 10")
        self.assertEqual(item.owner, 1)
        self.assertEqual(item.description, "Description 1")
        self.assertEqual(item.price, 10.0)

        self.assertTrue(self.db_manager.item_exists("Item 10"))

    def test_get_item_by_name(self):
        from utils.database_manager import InventoryItemTable

        # Test retrieving an existing item by item_id
        existing_item = InventoryItemTable(
            item_id=10, name="Item 10", owner=1, description="Description 1", price=10.0
        )
        with self.db_manager.Session() as session:
            session.add(existing_item)
            session.commit()

        # Retrieve the item from the database
        item = self.db_manager.get_item_by_name("Item 10")

        # Check if the item is not None
        self.assertIsNotNone(item)

        # Check if item attributes match the expected values
        self.assertEqual(item.item_id, 10)
        self.assertEqual(item.name, "Item 10")
        self.assertEqual(item.owner, 1)
        self.assertEqual(item.description, "Description 1")
        self.assertEqual(item.price, 10.0)

    def test_get_items_by_owner(self):
        from utils.database_manager import InventoryItemTable

        # Test retrieving items by owner
        item1 = InventoryItemTable(
            item_id=10, name="Item 10", owner=1, description="Description 1", price=10.0
        )
        item2 = InventoryItemTable(
            item_id=20, name="Item 20", owner=1, description="Description 2", price=20.0
        )
        item3 = InventoryItemTable(
            item_id=30, name="Item 30", owner=2, description="Description 3", price=30.0
        )
        with self.db_manager.Session() as session:
            session.add_all([item1, item2, item3])
            session.commit()

        # Retrieve items by owner
        items = self.db_manager.get_items_by_owner(owner=1)

        # Check if the correct number of items is returned,
        # note that two items are created when initializing the DataBaseManager
        self.assertEqual(len(items), 4)

        # Check if item attributes match the expected values
        self.assertEqual(items[2].item_id, 10)
        self.assertEqual(items[2].name, "Item 10")
        self.assertEqual(items[2].owner, 1)
        self.assertEqual(items[2].description, "Description 1")
        self.assertEqual(items[2].price, 10.0)

        self.assertEqual(items[3].item_id, 20)
        self.assertEqual(items[3].name, "Item 20")
        self.assertEqual(items[3].owner, 1)
        self.assertEqual(items[3].description, "Description 2")
        self.assertEqual(items[3].price, 20.0)

    def test_delete_item(self):
        from utils.database_manager import InventoryItemTable

        # Test deleting an existing item
        item = InventoryItemTable(
            item_id=10, name="Item 10", owner=1, description="Description 1", price=10.0
        )
        with self.db_manager.Session() as session:
            session.add(item)
            session.commit()

        # Delete the item
        self.db_manager.delete_item("Item 10")

        # Check if the item is deleted
        self.assertFalse(self.db_manager.item_exists("Item 10"))

    def test_remove_user_cascades_to_items(self):
        from utils.database_manager import InventoryItemTable, UserTable

        item = UserTable(
            id=10,
            username="testuser",
            full_name="Test UserTable",
            email="testuser@example.com",
            hashed_password="testpassword",
            disabled=False,
            is_admin=True,
        )
        with self.db_manager.Session() as session:
            session.add(item)
            session.commit()
        item = InventoryItemTable(
            item_id=10,
            name="Item 10",
            owner=10,
            description="Description 1",
            price=10.0,
        )
        with self.db_manager.Session() as session:
            session.add(item)
            session.commit()  # Test removing a user
        self.db_manager.remove_user("testuser")
        user = self.db_manager.get_user_by_username("testuser")
        self.assertIsNone(user)
        item = self.db_manager.get_item_by_name("Item 10")
        self.assertIsNone(item)
