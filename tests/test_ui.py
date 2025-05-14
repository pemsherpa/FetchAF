# Standard library imports
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Third-party imports
import streamlit as st

# Local imports
from app import (
    welcome_page,
    set_auth_cookie,
    clear_auth_cookie,
    verify_auth_cookie
)

class TestUI(unittest.TestCase):
    """Test cases for UI related functions."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        if not hasattr(st, 'session_state'):
            setattr(st, 'session_state', {})
        st.session_state.logged_in = False
        st.session_state.current_user = None
        self.mock_cookie_manager = MagicMock()

    @patch('app.stx.CookieManager')
    def test_set_auth_cookie(self, mock_cookie_manager_class):
        """Test setting authentication cookie."""
        mock_cookie_manager = MagicMock()
        mock_cookie_manager_class.return_value = mock_cookie_manager

        username = "test_user"
        set_auth_cookie(username)

        mock_cookie_manager.set.assert_called_once()
        args = mock_cookie_manager.set.call_args[0]
        self.assertEqual(args[0], "session_id")
        self.assertIsNotNone(args[1])

    @patch('app.stx.CookieManager')
    def test_clear_auth_cookie(self, mock_cookie_manager_class):
        """Test clearing authentication cookie."""
        mock_cookie_manager = MagicMock()
        mock_cookie_manager_class.return_value = mock_cookie_manager

        clear_auth_cookie()

        mock_cookie_manager.delete.assert_called_once_with("session_id")

    @patch('app.stx.CookieManager')
    @patch('app.get_db_engine')
    def test_verify_auth_cookie(self, mock_get_db, mock_cookie_manager_class):
        """Test verifying authentication cookie."""
        mock_cookie_manager = MagicMock()
        mock_cookie_manager_class.return_value = mock_cookie_manager

        mock_engine = MagicMock()
        mock_connection = MagicMock()
        mock_result = MagicMock()
        mock_get_db.return_value = mock_engine
        mock_engine.connect.return_value = mock_connection
        mock_connection.execute.return_value = mock_result

        # Test valid session
        mock_cookie_manager.get.return_value = "valid_session_id"
        mock_result.fetchone.return_value = ("test_user",)
        self.assertTrue(verify_auth_cookie())
        self.assertEqual(st.session_state.current_user, "test_user")
        self.assertTrue(st.session_state.logged_in)

        # Test invalid session
        mock_result.fetchone.return_value = None
        self.assertFalse(verify_auth_cookie())
        self.assertIsNone(st.session_state.current_user)
        self.assertFalse(st.session_state.logged_in)

    @patch('streamlit.markdown')
    def test_welcome_page_logged_out(self, mock_markdown):
        """Test welcome page when user is logged out."""
        st.session_state.logged_in = False
        welcome_page()
        mock_markdown.assert_called()

    @patch('streamlit.markdown')
    def test_welcome_page_logged_in(self, mock_markdown):
        """Test welcome page when user is logged in."""
        st.session_state.logged_in = True
        st.session_state.current_user = "test_user"
        welcome_page()
        mock_markdown.assert_called()

if __name__ == '__main__':
    unittest.main() 