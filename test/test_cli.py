from click.testing import CliRunner

import ctDNAtool.cli as cli


class Test_cli:
    def test_help(self):
        runner = CliRunner()
        result = runner.invoke(cli.cli)
        assert result.exit_code == 0
