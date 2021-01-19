import click
import tempfile
import logging

from .cli import (
    bin_genome,
    bin_genome_chromosome,
    generate_length,
    generate_length_end_seq,
    region_sum,
    convert_to_tsv_length,
)
from . import cli_common

logger = logging.getLogger()


@click.group()
@cli_common.quiet
@cli_common.debug
def cli_flow(quiet, debug):
    """ctDNAflow is a tool for running workflows based on the atomic commands found in ctDNAtool.

    The workflows are compositions of multiple commands from ctDNAtool, and are design for ease of use.

    EXAMPLES:

        ctDNAflow length-data-bed-bin <reference_genome_path> <BAM_file_path>

        ctDNAflow length-data-chr-bin <reference_genome_path> <BAM_file_path>
    """
    cli_common.setup_debugger(quiet, debug)


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
@cli_common.lower_bound
@cli_common.upper_bound
@cli_common.pickle_output
@click.pass_context
def length_data(
    ctx, genome_ref_file, bam_file, output_file, include_x, max_length, map_quality, lower_bound, upper_bound, pickle_output,
):
    """This command outputs the length data of a sample, given a genome reference file.
    The regions are collapsed

    EXAMPLE:

          ctDNAflow length-data <reference_genome_path> <BAM_file_path>
    """
    temp_bed_file = tempfile.NamedTemporaryFile().name
    temp_pickle_file = tempfile.NamedTemporaryFile().name
    temp_output_file = tempfile.NamedTemporaryFile().name

    if pickle_output:
        logger.info("Exporting to .pickle file")

    ctx.invoke(
        bin_genome_chromosome,
        genome_ref_file=genome_ref_file,
        output_file=temp_bed_file,
        include_x=include_x,
    )

    ctx.invoke(
        generate_length,
        bam_file=bam_file,
        bed_file=temp_bed_file,
        output_file=temp_pickle_file,
        max_length=max_length,
        map_quality=map_quality,
    )

    if pickle_output:
        ctx.invoke(region_sum, sample_file=temp_pickle_file, output_file=output_file)
    else:
        ctx.invoke(region_sum, sample_file=temp_pickle_file, output_file=temp_output_file)
        ctx.invoke(convert_to_tsv_length, input_file=temp_output_file, output_file=output_file, lower_bound=lower_bound, upper_bound=upper_bound)


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
@cli_common.lower_bound
@cli_common.upper_bound
@cli_common.pickle_output
@click.pass_context
def length_data_chr_bin(
    ctx, genome_ref_file, bam_file, output_file, include_x, max_length, map_quality, lower_bound, upper_bound, pickle_output
):
    """This command outputs the length data of a sample, given a genome reference file.
    The data is binned in chromosomes

    EXAMPLE:

          ctDNAflow length-data-chr-bin <reference_genome_path> <BAM_file_path>
    """
    temp_bed_file = tempfile.NamedTemporaryFile().name
    temp_output_file = tempfile.NamedTemporaryFile().name

    if pickle_output:
        logger.info("Exporting to .pickle file")

    ctx.invoke(
        bin_genome_chromosome,
        genome_ref_file=genome_ref_file,
        output_file=temp_bed_file,
        include_x=include_x,
    )

    if pickle_output:
        ctx.invoke(
            generate_length,
            bam_file=bam_file,
            bed_file=temp_bed_file,
            output_file=output_file,
            max_length=max_length,
            map_quality=map_quality,
        )
    else:
        ctx.invoke(
            generate_length,
            bam_file=bam_file,
            bed_file=temp_bed_file,
            output_file=temp_output_file,
            max_length=max_length,
            map_quality=map_quality,
        )
        ctx.invoke(convert_to_tsv_length, input_file=temp_output_file, output_file=output_file, lower_bound=lower_bound, upper_bound=upper_bound)


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
@cli_common.lower_bound
@cli_common.upper_bound
@cli_common.pickle_output
@click.pass_context
def length_data_bed_bin(
    ctx, genome_ref_file, bam_file, output_file, mbp, include_x, max_length, map_quality, lower_bound, upper_bound, pickle_output
):
    """This command outputs the length data of a sample, given a genome reference file.
    The data is binned in the provided mpb size

    EXAMPLE:

        ctDNAflow length-data-bed-bin <reference_genome_path> <BAM_file_path>"""

    if pickle_output:
        logger.info("Exporting to .pickle file")

    temp_bed_file = tempfile.NamedTemporaryFile().name
    temp_output_file = tempfile.NamedTemporaryFile().name

    ctx.invoke(
        bin_genome,
        genome_ref_file=genome_ref_file,
        output_file=temp_bed_file,
        mbp=mbp,
        include_x=include_x,
    )

    if pickle_output:
        ctx.invoke(
            generate_length,
            bam_file=bam_file,
            bed_file=temp_bed_file,
            output_file=temp_output_file,
            max_length=max_length,
            map_quality=map_quality,
        )
        ctx.invoke(convert_to_tsv_length, input_file=temp_output_file, output_file=output_file, lower_bound=lower_bound, upper_bound=upper_bound)
    else:
        ctx.invoke(
            generate_length,
            bam_file=bam_file,
            bed_file=temp_bed_file,
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
    temp_bed_file = tempfile.NamedTemporaryFile().name
    temp_pickle_file = tempfile.NamedTemporaryFile().name

    ctx.invoke(
        bin_genome_chromosome,
        genome_ref_file=genome_ref_file,
        output_file=temp_bed_file,
        include_x=include_x,
    )

    ctx.invoke(
        generate_length_end_seq,
        bam_file=bam_file,
        bed_file=temp_bed_file,
        output_file=temp_pickle_file,
        max_length=max_length,
        flank=flank,
        map_quality=map_quality,
    )

    ctx.invoke(region_sum, sample_file=temp_pickle_file, output_file=output_file)


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
    temp_bed_file = tempfile.NamedTemporaryFile().name

    ctx.invoke(
        bin_genome_chromosome,
        genome_ref_file=genome_ref_file,
        output_file=temp_bed_file,
        include_x=include_x,
    )
    ctx.invoke(
        generate_length_end_seq,
        bam_file=bam_file,
        bed_file=temp_bed_file,
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
    temp_bed_file = tempfile.NamedTemporaryFile().name

    ctx.invoke(
        bin_genome,
        genome_ref_file=genome_ref_file,
        output_file=temp_bed_file,
        mbp=mbp,
        include_x=include_x,
    )
    ctx.invoke(
        generate_length_end_seq,
        bam_file=bam_file,
        bed_file=temp_bed_file,
        output_file=output_file,
        max_length=max_length,
        map_quality=map_quality,
    )
