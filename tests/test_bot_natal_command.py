"""No-network, no-real-kernel smoke tests for opt-in Western natal preview."""
import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from datetime import datetime, date
from bot import natal_preview_command
from natal_pipeline import assemble_natal
from western_chart import chart_from_longitudes

def message(text,chat_type="private"):
    return SimpleNamespace(text=text,chat=SimpleNamespace(type=chat_type),answer=AsyncMock())

def fake_positions(_utc,_path):
    return chart_from_longitudes(
        {"Sun":270.4,"Moon":42.0,"Mars":358.5},
        verified_source="CI synthetic coordinates, no actual kernel"
    )

def synthetic_record():
    return assemble_natal(
        datetime(2005,12,23,8,37),"Asia/Yangon",
        16.85,96.15,"fixture.bsp",
        evaluation_date=date(2026,10,27),
        position_provider=fake_positions,
    )

class NatalCommandTests(unittest.IsolatedAsyncioTestCase):
    async def test_disabled_feature_never_calls_ephemeris(self):
        msg=message("/natal 2005-12-23 08:37 Asia/Yangon 16.85 96.15")
        with patch.dict(os.environ,{"ENABLE_WESTERN_NATAL":"0"},clear=True):
            with patch("bot.assemble_natal") as calculated:
                await natal_preview_command(msg)
                calculated.assert_not_called()
        self.assertIn("မဖွင့်ရသေး",msg.answer.await_args.args[0])
        self.assertNotIn("reply_markup",msg.answer.await_args.kwargs)

    async def test_review_not_approved_cannot_enable_natal(self):
        msg=message("/natal 2005-12-23 08:37 Asia/Yangon 16.85 96.15")
        with patch.dict(os.environ,{"ENABLE_WESTERN_NATAL":"1"},clear=True):
            with patch("bot.assemble_natal") as calculation:
                await natal_preview_command(msg)
                calculation.assert_not_called()
        self.assertIn("မဖွင့်ရသေး",msg.answer.await_args.args[0])
        self.assertNotIn("reply_markup",msg.answer.await_args.kwargs)

    async def test_group_birth_data_not_processed(self):
        msg=message("/natal 2005-12-23 08:37 Asia/Yangon 16.85 96.15","supergroup")
        await natal_preview_command(msg)
        self.assertIn("Private Chat",msg.answer.await_args.args[0])
        self.assertNotIn("reply_markup",msg.answer.await_args.kwargs)

    async def test_enabled_requires_existing_bsp(self):
        msg=message("/natal 2005-12-23 08:37 Asia/Yangon 16.85 96.15")
        with patch.dict(os.environ,{"ENABLE_WESTERN_NATAL":"1",
                                     "WESTERN_NATAL_REVIEW_APPROVED":"1",
                                     "JPL_EPHEMERIS_PATH":"/nonexistent/file.bsp"},clear=True):
            await natal_preview_command(msg)
        self.assertIn("Ephemeris",msg.answer.await_args.args[0])

    async def test_authorized_operator_preview_renders_checked_output(self):
        with TemporaryDirectory() as tmp:
            path=Path(tmp)/"fixture.bsp"
            path.write_bytes(b"only a fake file for CI; never a real kernel")
            msg=message("/natal 2005-12-23 08:37 Asia/Yangon 16.85 96.15")
            with patch.dict(os.environ,{"ENABLE_WESTERN_NATAL":"1",
                                     "WESTERN_NATAL_REVIEW_APPROVED":"1",
                                         "JPL_EPHEMERIS_PATH":str(path)},clear=True):
                with patch("bot.assemble_natal",return_value=synthetic_record()) as calculation:
                    await natal_preview_command(msg)
                    calculation.assert_called_once()
        body=msg.answer.await_args.args[0]
        kwargs=msg.answer.await_args.kwargs
        self.assertIn("Development Preview",body)
        self.assertIn("Whole Sign Houses",body)
        self.assertNotIn(chr(92)+"n",body)
        self.assertEqual(len(kwargs["reply_markup"].inline_keyboard[0]),2)
        self.assertEqual(kwargs["parse_mode"],"HTML")

    async def test_enabled_invalid_coordinates_fails_closed(self):
        with TemporaryDirectory() as tmp:
            path=Path(tmp)/"fixture.bsp"
            path.write_bytes(b"fixture placeholder")
            msg=message("/natal 2005-12-23 08:37 Asia/Yangon nan 96.15")
            with patch.dict(os.environ,{"ENABLE_WESTERN_NATAL":"1",
                                     "WESTERN_NATAL_REVIEW_APPROVED":"1",
                                         "JPL_EPHEMERIS_PATH":str(path)},clear=True):
                await natal_preview_command(msg)
        self.assertIn("မတွက်နိုင်",msg.answer.await_args.args[0])
        self.assertNotIn("reply_markup",msg.answer.await_args.kwargs)

if __name__=="__main__":
    unittest.main()
