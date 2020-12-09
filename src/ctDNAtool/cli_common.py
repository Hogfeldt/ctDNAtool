import click


def include_x(function):
    function = click.option(
        "-x",
        "--include-X",
        is_flag=True,
        help="Option for specifying whether the X chromosome should be included",
    )(function)

    return function


def max_length(function):
    function = click.option(
        "-m",
        "--max-length",
        default=500,
        type=click.IntRange(min=1),
        help="Maximum read length to be counted",
    )(function)

    return function


def map_quality(function):
    function = click.option(
        "-q",
        "--map-quality",
        default=20,
        type=click.IntRange(min=0),
        help="Minimum map quality",
    )(function)

    return function


def mbp(function):
    function = click.option(
        "-m",
        "--mbp",
        default=1.0,
        type=click.FloatRange(min=1e-06),
        help="Binning size given in mega Base Pairs",
    )(function)

    return function


def flank(function):
    function = click.option(
        "-f",
        "--flank",
        default=1,
        type=click.IntRange(min=1),
        help="Amount of base pairs on each end",  # TODO: description
    )

    return function


def stride(function):
    function = click.option(
        "-s",
        "--stride",
        default=1,
        type=click.IntRange(min=1),
        help="stride"  # TODO: description
    )

    return function

