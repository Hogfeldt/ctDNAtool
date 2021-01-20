from click.testing import CliRunner
import tempfile
import numpy as np

import ctDNAtool.cli as cli
import ctDNAtool.data as data
import ctDNAtool.combined_data as combined_data
import ctDNAtool.manipulations as mut


class Test_cli:
    def test_help(self):
        runner = CliRunner()
        result = runner.invoke(cli.cli)
        assert result.exit_code == 0

    def test_combine_data(self):
        runner = CliRunner()
        data1 = data.Data(np.array([1, 2, 3]), np.array(["region_id"]), None)
        data2 = data.Data(np.array([4, 5, 6]), np.array(["region_id"]), None)
        data1_file = tempfile.NamedTemporaryFile().name
        data.Data.write(data1, data1_file)
        data2_file = tempfile.NamedTemporaryFile().name
        data.Data.write(data2, data2_file)
        output_file = tempfile.NamedTemporaryFile(mode="w").name

        mut.combine_data(output_file, [data1_file, data2_file])
        #result = runner.invoke(cli.combine_data, ['-o ' + output_file, data1_file, data2_file])
        data_combined = combined_data.CombinedData.read(output_file)

        assert data_combined.IDs[0] == data1_file.split("/")[-1]
        assert data_combined.IDs[1] == data2_file.split("/")[-1]
        assert (data_combined.data[0].data == data1.data).all()
        assert (data_combined.data[1].data == data2.data).all()

