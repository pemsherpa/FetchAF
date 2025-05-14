# Standard library imports
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Local imports
from app import (
    hash_password,
    verify_credentials,
    user_exists,
    get_db_engine
)

class TestAuthentication(unittest.TestCase):
    """Test cases for authentication related functions."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_engine = MagicMock()
        self.mock_connection = MagicMock()
        self.mock_engine.connect.return_value = self.mock_connection

    def test_hash_password(self):
        """Test password hashing function."""
        password = "test_password123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        self.assertEqual(hash1, hash2)

        different_password = "different_password123"
        hash3 = hash_password(different_password)
        self.assertNotEqual(hash1, hash3)

    @patch('app.get_db_engine')
    def test_user_exists(self, mock_get_db):
        """Test user existence check."""
        mock_get_db.return_value = self.mock_engine
        mock_result = MagicMock()
        self.mock_connection.execute.return_value = mock_result

        # Test existing user
        mock_result.fetchone.return_value = (1,)
        self.assertTrue(user_exists("existing_user"))

        # Test non-existing user
        mock_result.fetchone.return_value = None
        self.assertFalse(user_exists("non_existing_user"))

    @patch('app.get_db_engine')
    def test_verify_credentials(self, mock_get_db):
        """Test credential verification."""
        mock_get_db.return_value = self.mock_engine
        mock_result = MagicMock()
        self.mock_connection.execute.return_value = mock_result

        test_password = "test_password123"
        hashed_password = hash_password(test_password)
        mock_result.fetchone.return_value = (hashed_password,)
        self.assertTrue(verify_credentials("test_user", test_password))

        # Test invalid password
        self.assertFalse(verify_credentials("test_user", "wrong_password"))

        # Test non-existing user
        mock_result.fetchone.return_value = None
        self.assertFalse(verify_credentials("non_existing_user", test_password))

    def test_get_db_engine(self):
        """Test database engine creation."""
        with patch('app.create_engine') as mock_create_engine:
            mock_create_engine.return_value = self.mock_engine
            engine = get_db_engine()
            self.assertEqual(engine, self.mock_engine)
            mock_create_engine.assert_called_once()

if __name__ == '__main__':
    unittest.main() 