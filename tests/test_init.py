"""Integration tests for lumen init command."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from lumen.cli import app
from lumen.config import Config, Credentials

runner = CliRunner()

_CREDS = Credentials()


def _test_config(**overrides) -> Config:
    base = Config(
        format="table",
        max_results=10,
        credentials=_CREDS,
    )
    for k, v in overrides.items():
        object.__setattr__(base, k, v)
    return base


def _invoke(*args: str, config: Config | None = None, prompts: list[str] | None = None):
    """Invoke the CLI, patching load_config and write_config.

    ``prompts`` is a list of Prompt.ask return values (in order), followed
    by a Confirm.ask return value (True/False).
    """
    cfg = config or _test_config()
    with patch("lumen.config.load_config", return_value=cfg):
        return runner.invoke(app, list(args))


# ---------------------------------------------------------------------------
# Helpers that patch Rich prompts directly
# ---------------------------------------------------------------------------


def _run_init(
    prompt_values: list[str],
    confirm_value: bool = True,
    config: Config | None = None,
) -> object:
    """Run `lumen init` with mocked Rich prompts."""
    cfg = config or _test_config()
    with (
        patch("lumen.config.load_config", return_value=cfg),
        patch(
            "lumen.commands.init.write_config", return_value=Path("/tmp/config.toml")
        ),
        patch("rich.prompt.Prompt.ask", side_effect=prompt_values),
        patch("rich.prompt.Confirm.ask", return_value=confirm_value),
    ):
        return runner.invoke(app, ["init"])


# ---------------------------------------------------------------------------
# Happy path: save configuration
# ---------------------------------------------------------------------------


class TestInitSave:
    def test_exits_0_on_save(self):
        result = _run_init(
            prompt_values=["sk-test-key", "user123", "zot-api-key", "10", "table"]
        )
        assert result.exit_code == 0

    def test_writes_config(self):
        with (
            patch("lumen.config.load_config", return_value=_test_config()),
            patch(
                "lumen.commands.init.write_config",
                return_value=Path("/tmp/config.toml"),
            ) as mock_write,
            patch(
                "rich.prompt.Prompt.ask",
                side_effect=["sk-test", "uid", "zot", "10", "table"],
            ),
            patch("rich.prompt.Confirm.ask", return_value=True),
        ):
            result = runner.invoke(app, ["init"])
        assert result.exit_code == 0
        mock_write.assert_called_once()

    def test_config_path_shown(self):
        result = _run_init(prompt_values=["", "", "", "10", "table"])
        assert result.exit_code == 0
        assert "/tmp/config.toml" in result.output

    def test_credentials_written(self):
        written_config = None

        def capture_write(cfg, path=None):
            nonlocal written_config
            written_config = cfg
            return Path("/tmp/config.toml")

        with (
            patch("lumen.config.load_config", return_value=_test_config()),
            patch("lumen.commands.init.write_config", side_effect=capture_write),
            patch(
                "rich.prompt.Prompt.ask",
                side_effect=["my-ss-key", "my-uid", "my-zot-key", "10", "table"],
            ),
            patch("rich.prompt.Confirm.ask", return_value=True),
        ):
            runner.invoke(app, ["init"])

        assert written_config is not None
        assert written_config.credentials.semantic_scholar_api_key == "my-ss-key"
        assert written_config.credentials.zotero_user_id == "my-uid"
        assert written_config.credentials.zotero_api_key == "my-zot-key"

    def test_max_results_written(self):
        written_config = None

        def capture(cfg, path=None):
            nonlocal written_config
            written_config = cfg
            return Path("/tmp/config.toml")

        with (
            patch("lumen.config.load_config", return_value=_test_config()),
            patch("lumen.commands.init.write_config", side_effect=capture),
            patch("rich.prompt.Prompt.ask", side_effect=["", "", "", "25", "list"]),
            patch("rich.prompt.Confirm.ask", return_value=True),
        ):
            runner.invoke(app, ["init"])

        assert written_config is not None
        assert written_config.max_results == 25
        assert written_config.format == "list"


# ---------------------------------------------------------------------------
# Abort path
# ---------------------------------------------------------------------------


class TestInitAbort:
    def test_abort_does_not_write(self):
        with (
            patch("lumen.config.load_config", return_value=_test_config()),
            patch("lumen.commands.init.write_config") as mock_write,
            patch("rich.prompt.Prompt.ask", side_effect=["", "", "", "10", "table"]),
            patch("rich.prompt.Confirm.ask", return_value=False),
        ):
            result = runner.invoke(app, ["init"])
        mock_write.assert_not_called()
        assert "Aborted" in result.output or result.exit_code == 0

    def test_abort_exit_code(self):
        result = _run_init(
            prompt_values=["", "", "", "10", "table"],
            confirm_value=False,
        )
        # Aborted — no error, just no write
        assert result.exit_code == 0


# ---------------------------------------------------------------------------
# Re-run pre-fills existing values
# ---------------------------------------------------------------------------


class TestInitRerun:
    def test_existing_credentials_available_as_defaults(self):
        existing = _test_config()
        existing.credentials = Credentials(
            semantic_scholar_api_key="existing-key",
            zotero_user_id="existing-uid",
            zotero_api_key="existing-zot",
        )
        written_config = None

        def capture(cfg, path=None):
            nonlocal written_config
            written_config = cfg
            return Path("/tmp/config.toml")

        # User presses Enter for all prompts — keeps existing values
        with (
            patch("lumen.config.load_config", return_value=existing),
            patch("lumen.commands.init.write_config", side_effect=capture),
            patch(
                "rich.prompt.Prompt.ask",
                side_effect=[
                    "existing-key",
                    "existing-uid",
                    "existing-zot",
                    "10",
                    "table",
                ],
            ),
            patch("rich.prompt.Confirm.ask", return_value=True),
        ):
            runner.invoke(app, ["init"])

        assert written_config is not None
        assert written_config.credentials.semantic_scholar_api_key == "existing-key"
