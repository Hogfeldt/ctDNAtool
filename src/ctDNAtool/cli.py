import click

from . import generators
from . import preprocessors
from . import manipulations
from .utils import tsv_reader


@click.group()
def cli():
    # Add debug info like:
    # click.echo('No matrices was given to collapse')
    # click.echo('Only one matrix was given to collapse')
    pass


@cli.command()
@click.argument("annotation_file")
@click.option("-k", "--region-size", default=10000, type=click.IntRange(min=0))
@click.option("--bed-file", default="transcription_start_sites.bed")
@click.option("--tss-file", default="transcription_start_sites.tsv")
def find_tss(annotation_file, region_size, bed_file, tss_file):
    preprocessors.find_tss(annotation_file, region_size, bed_file, tss_file)


@cli.command()
@click.argument("genome_ref_file")
@click.option("-o", "--output_file", default="genome_bins.bed")
@click.option("-m", "--mbp", default=1.0)  # TODO: this should only take values > 0
def bin_genome(genome_ref_file, output_file, mbp):
    # TODO: add option for switching between AUTOSOME_X and AUTOSOME
    preprocessors.bin_genome_Mbp(genome_ref_file, output_file, mbp)


@cli.command()
@click.argument("bam_file")
@click.argument("bed_file")
@click.option("-o", "--output-file", default="length_matrix.pickle")
@click.option("-m", "--max-length", default=500, type=click.IntRange(min=1))
def generate_length(bam_file, bed_file, output_file, max_length):
    generators.length_matrix(bam_file, bed_file, output_file, max_length)


@cli.command()
@click.argument("bam_file")
@click.argument("bed_file")
@click.argument("reference_genome")
@click.option("-o", "--output-file", default="length_matrix.pickle")
@click.option("-m", "--max-length", default=500, type=click.IntRange(min=1))
@click.option("-f", "--flank", default=1, type=click.IntRange(min=1))
def generate_length_end_seq(
    bam_file, bed_file, reference_genome, output_file, max_length, flank
):
    generators.length_end_seqs(
        bam_file, bed_file, reference_genome, output_file, max_length, flank
    )


@cli.command()
@click.argument("bam_file")
@click.argument("bed_file")
@click.argument("reference_genome")
@click.option("-o", "--output-file", default="length_matrix.pickle")
@click.option("-m", "--max-length", default=500, type=click.IntRange(min=1))
@click.option("-f", "--flank", default=1, type=click.IntRange(min=1))
def generate_mate_length_end_seq(
    bam_file, bed_file, reference_genome, output_file, max_length, flank
):
    generators.mate_length_end_seqs(
        bam_file, bed_file, reference_genome, output_file, max_length, flank
    )


@cli.command()
@click.argument("sample_files", nargs=-1)
@click.option("-o", "--output-file", default="collapsed_samples.pickle")
@click.option("--uint32", is_flag=True)
def sample_sum(sample_files, output_file, uint32):
    if len(sample_files) > 0:
        manipulations.sample_sum(sample_files, output_file, uint32)


@cli.command()
@click.argument("sample_file")
@click.option("-o", "--output-file", default="collapsed_sample.pickle")
def region_sum(sample_file, output_file):
    manipulations.region_sum(sample_file, output_file)


@cli.command()
@click.argument("input_sample")
@click.argument("ids_file")
@click.option("-o", "--output-file", default="subset_sample.pickle")
def pick_subset(input_sample, ids_file, output_file):
    ids = list()
    with open(ids_file) as fp:
        for line in tsv_reader(fp):
            if line[0].startswith("#"):
                continue
            ids.append(line[0])
    manipulations.pick_subset(input_sample, output_file, ids)


@cli.command()
@click.argument("input_matrix")
@click.option("-o", "--output-file", default="binned_matrix.pickle")
@click.option("-b", "--bin-size", default=1, type=click.IntRange(min=1))
@click.option("-s", "--stride", default=1, type=click.IntRange(min=1))
def binning(input_matrix, output_file, bin_size, stride):
    manipulations.binning(input_matrix, output_file, bin_size, stride)
