import unittest
import sys
import os

# Add the parent directory to the path so we can import from app.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import functions from app.py to test
from app import hash_password, user_exists

class TestAppFunctions(unittest.TestCase):
    """Test case for the app functions."""
    
    def test_hash_password(self):
        """Test that the hash_password function returns a string of expected length."""
        # Act
        hashed = hash_password("test_password")
        
        # Assert
        self.assertIsInstance(hashed, str)
        self.assertEqual(len(hashed), 64)  # SHA-256 produces a 64-character hex string
    
    def test_hash_password_consistency(self):
        """Test that hash_password returns consistent results for the same input."""
        # Act
        hash1 = hash_password("test_password")
        hash2 = hash_password("test_password")
        
        # Assert
        self.assertEqual(hash1, hash2)
    
    def test_hash_password_different_inputs(self):
        """Test that hash_password returns different results for different inputs."""
        # Act
        hash1 = hash_password("password1")
        hash2 = hash_password("password2")
        
        # Assert
        self.assertNotEqual(hash1, hash2)

    # This test will need to be updated with mocking for the database connection
    @unittest.skip("Needs database connection mocking")
    def test_user_exists(self):
        """Test the user_exists function with mocked database."""
        # TODO: Implement with proper database mocking
        pass

if __name__ == '__main__':
    unittest.main() 