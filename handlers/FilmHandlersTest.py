import unittest
import asyncio
from unittest.mock import patch, Mock, AsyncMock, MagicMock
from FilmHandlers import FilmHandlers


class TestFilmHandlers(unittest.TestCase):

    @patch('FilmHandlers.FilmFetch.standard_request', return_value="data1")
    @patch('FilmHandlers.InlineKeyboardButton', return_value="button1")
    @patch('FilmHandlers.InlineKeyboardMarkup', return_value="markup1")
    @patch('FilmHandlers.make_film_card', return_value=("p1", "c1", "b1"))
    def test_random_film(self, mock_make_film_card, mock_button, mock_markup, mock_fetch):
        mock_update = Mock()
        mock_reply = AsyncMock()
        mock_update.message.reply_photo = mock_reply

        mock_logger = Mock()
        test_instance = FilmHandlers("states1", mock_logger)
        asyncio.run(test_instance.random_film(mock_update, "param2"))

        mock_fetch.assert_called_once()
        mock_make_film_card.assert_called_once()
        mock_reply.assert_awaited_once_with(photo="p1", caption="c1", reply_markup="markup1")
        mock_markup.assert_called_once()
        mock_logger.error.assert_not_called()

    @patch('FilmHandlers.FilmFetch.standard_request', side_effect=Exception("test exception"))
    @patch('FilmHandlers.InlineKeyboardButton', return_value="button1")
    def test_random_film_exception(self, mock_button, mock_fetch):
        mock_logger = Mock()
        test_instance = FilmHandlers("states1", mock_logger)
        asyncio.run(test_instance.random_film("param1", "param2"))

        mock_fetch.assert_called_once()
        mock_logger.error.assert_called_once_with("ERROR occurred")

    @patch('FilmHandlers.InlineKeyboardMarkup', return_value="markup1")
    @patch('FilmHandlers.InlineKeyboardButton', return_value="button1")
    def test_send_film(self, mock_button, mock_markup):
        mock_update = Mock()
        mock_reply = AsyncMock()
        mock_update.message.reply_text = mock_reply

        mock_states = Mock(FIND_NAMES="value")

        mock_logger = Mock()
        test_instance = FilmHandlers(mock_states, mock_logger)
        result = asyncio.run(test_instance.send_film(mock_update, "param2"))

        mock_reply.assert_awaited()
        mock_markup.assert_called_once()
        mock_logger.info.assert_called_once()
        self.assertEqual(result, "value")


if __name__ == '__main__':
    unittest.main()
