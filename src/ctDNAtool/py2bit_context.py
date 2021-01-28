import py2bit


class Py2bitContext:
    """Context manager wrapper for py2bit, for use with open()"""

    def __init__(self, ref_genome_file):
        print("Initiate Context manager")
        self.tb = py2bit.open(ref_genome_file)

    def __enter__(self):
        print("opens")
        return self.tb

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("closes")
        self.tb.close()
