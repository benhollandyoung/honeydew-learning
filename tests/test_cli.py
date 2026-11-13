from importlib.metadata import version

from typer.testing import CliRunner

from honeydew_learning.cli import app

runner = CliRunner()

def test_version_command() -> None:
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert version("honeydew_learning") in result.output

#def test_status_command() -> None:
#    result = runner.invoke(app, ["status"])
#
 #   assert result.exit_code == 0
#    assert "Agent: not running" in result.output

