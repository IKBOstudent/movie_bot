import unittest
from unittest.mock import patch, Mock, AsyncMock, MagicMock
import asyncio
from CategoryHandlers import CategoryHandler


class TestsCategoryHandler(unittest.TestCase):
    @patch('CategoryHandlers.FilmFetch.cached_request', return_value="data1")
    @patch('CategoryHandlers.CategoryHandler.createButtons', return_value="markup1")
    def test_response_categ(self, mock_buttons, mock_fetch):
        mock_update = Mock()
        mock_reply = AsyncMock()
        mock_update.message.reply_text = mock_reply

        mock_state = Mock(FIND_CATEGORY="test_result")
        mock_logger = Mock()
        test_instance = CategoryHandler(mock_state, mock_logger)
        result = asyncio.run(test_instance.response_categories(mock_update, "some_params"))

        mock_fetch.assert_called_once()
        mock_buttons.assert_called_once()
        mock_reply.assert_awaited_once_with(text="Жанры:", reply_markup="markup1")
        mock_logger.assert_not_called()
        self.assertEqual(result, "test_result")

    @patch('CategoryHandlers.FilmFetch.cached_request', side_effect=Exception("test exception"))
    def test_response_categ_exception(self, mock_fetch):
        mock_logger = Mock()
        test_instance = CategoryHandler("state_excep", mock_logger)
        asyncio.run(test_instance.response_categories("param1", "param2"))
        mock_fetch.assert_called_once()
        mock_logger.error.assert_called_once_with("ERROR occurred:")

    @patch('CategoryHandlers.FilmFetch.cached_request', return_value="data1")
    @patch('CategoryHandlers.CategoryHandler.createBtnFilms', return_value="markup1")
    def test_response_film_by_categ(self, mock_buttons, mock_fetch):
        mock_update = Mock()
        mock_reply_text = AsyncMock()
        mock_reply_markup = AsyncMock()

        mock_update.callback_query.edit_message_text = mock_reply_text
        mock_update.callback_query.edit_message_reply_markup = mock_reply_markup

        mock_state = Mock(SEND_BY_CATEG="state")
        mock_logger = Mock()
        test_instance = CategoryHandler(mock_state, mock_logger)

        result = asyncio.run(test_instance.response_film_by_categ(mock_update))

        mock_fetch.assert_called_once()
        mock_buttons.assert_called_once()

        mock_reply_text.assert_called_once_with(text="Выберите фильм")
        mock_reply_markup.assert_called_once_with(reply_markup="markup1")
        mock_logger.assert_not_called()
        self.assertEqual(result, None)

    @patch('CategoryHandlers.FilmFetch.cached_request', side_effect=Exception("test exception"))
    def test_response_film_by_categ_exception(self, mock_fetch):
        mock_logger = Mock()
        test_instance = CategoryHandler("state_excep", mock_logger)
        asyncio.run(test_instance.response_film_by_categ("param1"))
        mock_fetch.assert_called_once()
        mock_logger.error.assert_called_once_with("ERROR occurred:")


