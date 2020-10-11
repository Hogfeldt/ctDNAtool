from unittest import TestCase
from click.testing import CliRunner

import ctDNAtool.cli as cli


class Test_cli(TestCase):
    def test_help(self):
        runner = CliRunner()
        result = runner.invoke(cli.cli)
        self.assertTrue(result.exit_code == 0)
