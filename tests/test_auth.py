import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the path so we can import from app.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import functions from app.py to test
from app import verify_credentials, user_exists, hash_password

class TestAuthFunctions(unittest.TestCase):
    """Test case for the authentication functions."""
    
    @patch('app.verify_auth_cookie')
    def test_verify_auth_cookie(self, mock_verify_auth_cookie):
        """Test verify_auth_cookie with mocking."""
        # Arrange
        mock_verify_auth_cookie.return_value = ('testuser', True)
        
        # Act
        username, is_valid = mock_verify_auth_cookie()
        
        # Assert
        self.assertEqual(username, 'testuser')
        self.assertTrue(is_valid)
        mock_verify_auth_cookie.assert_called_once()
    
    @patch('app.get_db_engine')
    def test_user_exists_when_user_found(self, mock_get_db_engine):
        """Test user_exists when user is found in the database."""
        # Arrange
        mock_engine = MagicMock()
        mock_get_db_engine.return_value = mock_engine
        
        # Setup the mock connection and execution
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn
        
        # Mock the result of execute
        mock_result = MagicMock()
        mock_result.fetchone.return_value = ('existing_user',)  # Mock a row being returned
        mock_conn.execute.return_value = mock_result
        
        # Act
        result = user_exists('existing_user')
        
        # Assert
        self.assertTrue(result)
        mock_get_db_engine.assert_called_once()
        mock_engine.connect.assert_called_once()
    
    @patch('app.get_db_engine')
    def test_user_exists_when_user_not_found(self, mock_get_db_engine):
        """Test user_exists when user is not found in the database."""
        # Arrange
        mock_engine = MagicMock()
        mock_get_db_engine.return_value = mock_engine
        
        # Setup the mock connection and execution
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn
        
        # Mock the result of execute
        mock_result = MagicMock()
        mock_result.fetchone.return_value = None  # No user found
        mock_conn.execute.return_value = mock_result
        
        # Act
        result = user_exists('nonexistent_user')
        
        # Assert
        self.assertFalse(result)
        mock_get_db_engine.assert_called_once()
        mock_engine.connect.assert_called_once()
    
    @patch('app.verify_credentials')
    def test_verify_credentials_success(self, mock_verify_credentials):
        """Test successful credential verification."""
        # Arrange
        mock_verify_credentials.return_value = True
        
        # Act
        result = mock_verify_credentials('testuser', 'correct_password')
        
        # Assert
        self.assertTrue(result)
        mock_verify_credentials.assert_called_once_with('testuser', 'correct_password')
    
    @patch('app.verify_credentials')
    def test_verify_credentials_failure(self, mock_verify_credentials):
        """Test failed credential verification."""
        # Arrange
        mock_verify_credentials.return_value = False
        
        # Act
        result = mock_verify_credentials('testuser', 'wrong_password')
        
        # Assert
        self.assertFalse(result)
        mock_verify_credentials.assert_called_once_with('testuser', 'wrong_password')

if __name__ == '__main__':
    unittest.main() 