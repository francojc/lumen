"""Tests for BaseClient._get error handling and _http_error_message helper.

Strategy
--------
- Test _http_error_message directly for all status-code branches.
- Test _get behaviour against a real httpx.MockTransport to exercise the
  retry loop, HTTPStatusError conversion, and circuit-breaker paths.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from lumen.clients.arxiv import ArxivClient
from lumen.clients.base import _http_error_message
from lumen.exceptions import SourceError

# ---------------------------------------------------------------------------
# _http_error_message — unit tests
# ---------------------------------------------------------------------------


class TestHttpErrorMessage:
    def test_401_message(self) -> None:
        msg, hint = _http_error_message("TestSource", 401)
        assert "401" in msg
        assert "lumen init" in hint

    def test_403_message(self) -> None:
        msg, hint = _http_error_message("TestSource", 403)
        assert "403" in msg
        assert "API key" in hint
        assert "lumen init" in hint

    def test_404_message(self) -> None:
        msg, hint = _http_error_message("TestSource", 404)
        assert "404" in msg
        assert "not exist" in hint

    def test_429_message(self) -> None:
        msg, hint = _http_error_message("TestSource", 429)
        assert "429" in msg
        assert "lumen init" in hint

    def test_500_message(self) -> None:
        msg, hint = _http_error_message("TestSource", 500)
        assert "500" in msg
        assert "temporarily unavailable" in hint

    def test_502_message(self) -> None:
        msg, hint = _http_error_message("TestSource", 502)
        assert "502" in msg

    def test_unknown_status(self) -> None:
        msg, hint = _http_error_message("TestSource", 418)
        assert "418" in msg
        assert "lumen doctor" in hint

    def test_source_name_in_message(self) -> None:
        msg, _ = _http_error_message("ArxivClient", 403)
        assert "ArxivClient" in msg


# ---------------------------------------------------------------------------
# BaseClient._get — via ArxivClient with respx mocking
# ---------------------------------------------------------------------------

_ARXIV_URL = "https://export.arxiv.org/api/query"


@pytest.mark.asyncio
class TestBaseClientGet:
    async def test_403_raises_source_error(self) -> None:
        with respx.mock:
            respx.get(_ARXIV_URL).mock(return_value=httpx.Response(403))
            client = ArxivClient()
            with pytest.raises(SourceError) as exc_info:
                await client._get(_ARXIV_URL)
        assert "403" in exc_info.value.message
        assert "API key" in exc_info.value.suggestion

    async def test_404_raises_source_error(self) -> None:
        with respx.mock:
            respx.get(_ARXIV_URL).mock(return_value=httpx.Response(404))
            client = ArxivClient()
            with pytest.raises(SourceError) as exc_info:
                await client._get(_ARXIV_URL)
        assert "404" in exc_info.value.message

    async def test_500_retries_then_raises(self) -> None:
        """500 is retried up to _MAX_RETRIES times then raises SourceError."""
        with respx.mock:
            respx.get(_ARXIV_URL).mock(return_value=httpx.Response(500))
            client = ArxivClient()
            with pytest.raises(SourceError) as exc_info:
                await client._get(_ARXIV_URL)
        assert "500" in exc_info.value.message
        assert "temporarily" in exc_info.value.suggestion

    async def test_200_returns_response(self) -> None:
        with respx.mock:
            respx.get(_ARXIV_URL).mock(return_value=httpx.Response(200, text="<feed/>"))
            client = ArxivClient()
            resp = await client._get(_ARXIV_URL)
        assert resp.status_code == 200

    async def test_network_error_raises_source_error(self) -> None:
        with respx.mock:
            respx.get(_ARXIV_URL).mock(side_effect=httpx.ConnectError("refused"))
            client = ArxivClient()
            with pytest.raises(SourceError) as exc_info:
                await client._get(_ARXIV_URL)
        assert "network error" in exc_info.value.message.lower()
        assert client._circuit_open is True

    async def test_circuit_open_raises_immediately(self) -> None:
        """A client with circuit open should raise without making any request."""
        with respx.mock:
            route = respx.get(_ARXIV_URL).mock(
                return_value=httpx.Response(200, text="ok")
            )
            client = ArxivClient()
            client._circuit_open = True
            with pytest.raises(SourceError) as exc_info:
                await client._get(_ARXIV_URL)
        assert route.called is False
        assert "circuit" in exc_info.value.message.lower()

    async def test_source_error_not_swallowed(self) -> None:
        """A SourceError raised inside the loop must propagate unchanged."""
        with respx.mock:
            respx.get(_ARXIV_URL).mock(return_value=httpx.Response(403))
            client = ArxivClient()
            with pytest.raises(SourceError) as exc_info:
                await client._get(_ARXIV_URL)
        # Should be the 403-specific message, not a generic wrapper
        assert "Forbidden" in exc_info.value.message
