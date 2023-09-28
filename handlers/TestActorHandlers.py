import unittest
import asyncio
from unittest.mock import patch, Mock, AsyncMock, MagicMock
from ActorHandlers import ActorHandlers
from utils.fetch import FilmFetch

class TestActorHandlers(unittest.TestCase):
    @patch('ActorHandlers.FilmFetch.cached_request', return_value={"total":"1", "docs":[{"name":"Film1", "id":"2"}]})
    @patch('ActorHandlers.InlineKeyboardButton', side_effect=["button1", "button2"])
    @patch('ActorHandlers.InlineKeyboardMarkup', return_value="markup1")
    def test_response_actors(self, mock_markup, mock_button, mock_fetch):
        mock_update = Mock()
        mock_reply = AsyncMock()
        mock_update.message.reply_text = mock_reply

        mock_logger = Mock()
        test_instance = ActorHandlers("states1", mock_logger)
        mock_button.assert_called_with("Отмена",
                                       callback_data="cancel")
        asyncio.run(test_instance.response_actors(mock_update, "param2"))

        mock_fetch.assert_called_once()
        mock_button.assert_called_with(text="Film1",
                                       callback_data="2")
        mock_markup.assert_called_once_with([["button2"],["button1"]])
        mock_reply.assert_awaited_once_with("По вашему запросу найдено результатов: 1", reply_markup="markup1")

        mock_logger.error.assert_not_called()

    @patch('ActorHandlers.FilmFetch.cached_request',
           side_effect=Exception)
    @patch('ActorHandlers.InlineKeyboardButton',
           side_effect=["button1", "button2", "button3"])
    @patch('ActorHandlers.InlineKeyboardMarkup', return_value="markup1")
    def test_response_actors_bad_fetch(self, mock_markup, mock_button, mock_fetch):
        mock_update = Mock()
        mock_reply = AsyncMock()
        mock_update.message.reply_text = mock_reply

        mock_logger = Mock()
        test_instance = ActorHandlers("states1", mock_logger)
        mock_button.assert_called_with("Отмена",
                                       callback_data="cancel")
        asyncio.run(test_instance.response_actors(mock_update, "param2"))

        mock_fetch.assert_called_once()
        mock_markup.assert_not_called()
        mock_reply.assert_not_awaited()

        mock_logger.error.assert_called_with("ERROR occurred:")

    @patch('ActorHandlers.FilmFetch.cached_request',
           side_effect=Exception)
    @patch('ActorHandlers.InlineKeyboardButton',
           side_effect=["button1", "button2", "button3"])
    @patch('ActorHandlers.InlineKeyboardMarkup', return_value="markup1")
    def test_response_actors_bad_fetch(self, mock_markup, mock_button,
                                       mock_fetch):
        mock_update = Mock()
        mock_reply = AsyncMock()
        mock_update.message.reply_text = mock_reply

        mock_logger = Mock()
        mock_states = Mock(FIND_ACTORS = 1)
        test_instance = ActorHandlers(mock_states, mock_logger)
        mock_button.assert_called_with("Отмена",
                                       callback_data="cancel")
        result = asyncio.run(test_instance.send_actor(mock_update, "param2"))

        mock_markup.assert_called()
        mock_reply.assert_awaited_once_with("Какого актёра вы хотите найти?",
                                            reply_markup="markup1")

        mock_logger.info.assert_called_with("SENT reply with state {FIND_ACTORS}")
        self.assertEqual(result, 1)


