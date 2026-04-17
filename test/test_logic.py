from unittest.mock import Mock, patch
import unittest

from brain.logic import handle_command


class LogicTests(unittest.TestCase):
    def test_time_command_returns_time_response(self):
        response = handle_command("what time is it")
        self.assertIn("It is", response.text)
        self.assertTrue(response.understood)

    def test_unsafe_command_is_blocked(self):
        response = handle_command("shutdown my pc")
        self.assertIn("will not run high-risk system commands", response.text)
        self.assertFalse(response.understood)

    @patch("brain.logic.open_application")
    def test_open_app_command_routes_to_action(self, open_application):
        open_application.return_value = Mock(message="Opening notepad.", performed=True)

        response = handle_command("open notepad")

        open_application.assert_called_once_with("notepad")
        self.assertEqual(response.text, "Opening notepad.")

    @patch("brain.logic.search_web")
    def test_search_command_routes_to_web_search(self, search_web):
        search_web.return_value = Mock(
            message="Searching the web for python.", performed=True
        )

        response = handle_command("search for python")

        search_web.assert_called_once_with("python")
        self.assertEqual(response.text, "Searching the web for python.")


if __name__ == "__main__":
    unittest.main()
