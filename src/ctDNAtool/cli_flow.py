import click
import tempfile

from .cli import (
    bin_genome,
    bin_genome_chromosome,
    generate_length,
    generate_length_end_seq,
    region_sum,
)
from . import cli_common


@click.group()
def cli_flow():
    """ctDNAflow is a tool for running workflows based on the atomic commands found in ctDNAtool.

    The workflows are compositions of multiple commands from ctDNAtool, and are design for ease of use.

    EXAMPLES:

        ctDNAflow length-data-bed-bin <reference_genome_path> <BAM_file_path>

        ctDNAflow length-data-chr-bin <reference_genome_path> <BAM_file_path>
    """
    pass


@cli_flow.command()
@click.argument("genome_ref_file")
@click.argument("bam_file")
@click.option(
    "-o",
    "--output-file",
    default="length_matrix.pickle",
    help="Output file name. Default output to length_matrix.pickle",
)
@cli_common.include_x
@cli_common.max_length
@cli_common.map_quality
@click.pass_context
def length_data(
    ctx, genome_ref_file, bam_file, output_file, include_x, max_length, map_quality
):
    """This command outputs the length data of a sample, given a genome reference file.
    The regions are collapsed

    EXAMPLE:

          ctDNAflow length-data <reference_genome_path> <BAM_file_path>
    """
    temp_bed_file = tempfile.NamedTemporaryFile()
    temp_pickle_file = tempfile.NamedTemporaryFile()

    ctx.invoke(
        bin_genome_chromosome,
        genome_ref_file=genome_ref_file,
        output_file=temp_bed_file.name,
        include_x=include_x,
    )

    ctx.invoke(
        generate_length,
        bam_file=bam_file,
        bed_file=temp_bed_file.name,
        output_file=temp_pickle_file.name,
        max_length=max_length,
        map_quality=map_quality,
    )

    ctx.invoke(
        region_sum,
        sample_file=temp_pickle_file.name,
        output_file=output_file,
    )


@cli_flow.command()
@click.argument("genome_ref_file")
@click.argument("bam_file")
@click.option(
    "-o",
    "--output-file",
    default="length_matrix.pickle",
    help="Output file name. Default output to length_matrix.pickle",
)
@cli_common.include_x
@cli_common.max_length
@cli_common.map_quality
@click.pass_context
def length_data_chr_bin(
    ctx, genome_ref_file, bam_file, output_file, include_x, max_length, map_quality
):
    """This command outputs the length data of a sample, given a genome reference file.
    The data is binned in chromosomes

    EXAMPLE:

          ctDNAflow length-data-chr-bin <reference_genome_path> <BAM_file_path>
    """
    temp_bed_file = tempfile.NamedTemporaryFile()

    ctx.invoke(
        bin_genome_chromosome,
        genome_ref_file=genome_ref_file,
        output_file=temp_bed_file.name,
        include_x=include_x,
    )
    ctx.invoke(
        generate_length,
        bam_file=bam_file,
        bed_file=temp_bed_file.name,
        output_file=output_file,
        max_length=max_length,
        map_quality=map_quality,
    )


@cli_flow.command()
@click.argument("genome_ref_file")
@click.argument("bam_file")
@click.option(
    "-o",
    "--output-file",
    default="length_matrix.pickle",
    help="Output file name. Default output to length_matrix.pickle",
)
@cli_common.mbp
@cli_common.include_x
@cli_common.max_length
@cli_common.map_quality
@click.pass_context
def length_data_bed_bin(
    ctx, genome_ref_file, bam_file, output_file, mbp, include_x, max_length, map_quality
):
    """This command outputs the length data of a sample, given a genome reference file.
    The data is binned in the provided mpb size

    EXAMPLE:

        ctDNAflow length-data-bed-bin <reference_genome_path> <BAM_file_path>"""
    temp_bed_file = tempfile.NamedTemporaryFile()

    ctx.invoke(
        bin_genome,
        genome_ref_file=genome_ref_file,
        output_file=temp_bed_file.name,
        mbp=mbp,
        include_x=include_x,
    )
    ctx.invoke(
        generate_length,
        bam_file=bam_file,
        bed_file=temp_bed_file.name,
        output_file=output_file,
        max_length=max_length,
        map_quality=map_quality,
    )


@cli_flow.command()
@click.argument("genome_ref_file")
@click.argument("bam_file")
@click.option(
    "-o",
    "--output-file",
    default="length_seq_matrix.pickle",
    help="Output file name. Default output to length_seq_matrix.pickle",
)
@cli_common.include_x
@cli_common.max_length
@cli_common.map_quality
@click.option("-f", "--flank", default=1, type=click.IntRange(min=1))
@click.pass_context
def length_seq_data(
    ctx,
    genome_ref_file,
    bam_file,
    output_file,
    include_x,
    max_length,
    flank,
    map_quality,
):
    """This command outputs the end sequence and length data of a sample, given a genome reference file.
    Chromosome regions is collapsed

    EXAMPLE:

          ctDNAflow length-seq-data <reference_genome_path> <BAM_file_path>
    """
    temp_bed_file = tempfile.NamedTemporaryFile()
    temp_pickle_file = tempfile.NamedTemporaryFile()

    ctx.invoke(
        bin_genome_chromosome,
        genome_ref_file=genome_ref_file,
        output_file=temp_bed_file.name,
        include_x=include_x,
    )

    ctx.invoke(
        generate_length_end_seq,
        bam_file=bam_file,
        bed_file=temp_bed_file.name,
        output_file=temp_pickle_file.name,
        max_length=max_length,
        flank=flank,
        map_quality=map_quality,
    )

    ctx.invoke(
        region_sum,
        sample_file=temp_pickle_file.name,
        output_file=output_file,
    )


@cli_flow.command()
@click.argument("genome_ref_file")
@click.argument("bam_file")
@click.option(
    "-o",
    "--output-file",
    default="length_seq_matrix.pickle",
    help="Output file name. Default output to length_seq_matrix.pickle",
)
@cli_common.include_x
@cli_common.max_length
@cli_common.map_quality
@click.option("-f", "--flank", default=1, type=click.IntRange(min=1))
@click.pass_context
def length_seq_data_chr_bin(
    ctx,
    genome_ref_file,
    bam_file,
    output_file,
    include_x,
    max_length,
    flank,
    map_quality,
):
    """This command outputs the end sequence and length data of a sample, given a genome reference file.
    The data is binned in chromosomes

    EXAMPLE:

          ctDNAflow length-seq-data-chr-bin <reference_genome_path> <BAM_file_path>
    """
    temp_bed_file = tempfile.NamedTemporaryFile()

    ctx.invoke(
        bin_genome_chromosome,
        genome_ref_file=genome_ref_file,
        output_file=temp_bed_file.name,
        include_x=include_x,
    )
    ctx.invoke(
        generate_length_end_seq,
        bam_file=bam_file,
        bed_file=temp_bed_file.name,
        output_file=output_file,
        max_length=max_length,
        flank=flank,
        map_quality=map_quality,
    )


@cli_flow.command()
@click.argument("genome_ref_file")
@click.argument("bam_file")
@click.option(
    "-o",
    "--output-file",
    default="length_matrix.pickle",
    help="Output file name. Default output to length_matrix.pickle",
)
@cli_common.mbp
@cli_common.include_x
@cli_common.max_length
@cli_common.map_quality
@click.pass_context
def length_seq_data_bed_bin(
    ctx, genome_ref_file, bam_file, output_file, mbp, include_x, max_length, map_quality
):
    """This command outputs the length data of a sample, given a genome reference file.
    The data is binned in the provided mpb size

    EXAMPLE:

        ctDNAflow length-data-bed-bin <reference_genome_path> <BAM_file_path>"""
    temp_bed_file = tempfile.NamedTemporaryFile()

    ctx.invoke(
        bin_genome,
        genome_ref_file=genome_ref_file,
        output_file=temp_bed_file.name,
        mbp=mbp,
        include_x=include_x,
    )
    ctx.invoke(
        generate_length_end_seq,
        bam_file=bam_file,
        bed_file=temp_bed_file.name,
        output_file=output_file,
        max_length=max_length,
        map_quality=map_quality,
    )
