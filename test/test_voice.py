import unittest
from unittest.mock import patch

import speech.speak as speak_module


class SpeakTests(unittest.TestCase):
    @patch("speech.speak._speak_with_windows_voice", return_value=False)
    @patch("speech.speak._speak_with_piper", return_value=False)
    @patch("builtins.print")
    def test_speak_without_piper_or_local_voice_only_prints_status(
        self, fake_print, fake_piper, fake_local_voice
    ):
        speak_module._LAST_VOICE_MODE = None
        speak_module.speak("Testing fallback speech")
        fake_piper.assert_called_once()
        fake_local_voice.assert_called_once()
        self.assertEqual(fake_print.call_count, 2)


if __name__ == "__main__":
    unittest.main()
