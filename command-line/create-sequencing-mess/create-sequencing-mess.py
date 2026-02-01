#! /usr/bin/env python3
"""
create-sequencing-mess.py - Generate messy sequencing files for training exercises.

This script creates dummy sequencing files with realistic naming patterns
and configurable levels of chaos for command-line training exercises.
"""
import logging
import random
import shutil
import sys

from pathlib import Path

import rich
import rich.console
import rich.traceback
import rich_click as click
from rich.logging import RichHandler

VERSION = "0.1.0"

# Default values - customize these for your training context
DEFAULT_ORGANISMS = ["FLU", "COVID", "RSV", "MPOX", "MEAS"]
DEFAULT_ORGS = ["WPHL", "WY", "UW", "WSLV", "CDC", "APHL"]
DEFAULT_TECHS = ["ILLUMINA", "ONT", "PACBIO"]
DEFAULT_YEARS = ["2019", "2020", "2021", "2022", "2023", "2024", "2025"]

# Set up Rich
stderr = rich.console.Console(stderr=True)
rich.traceback.install(console=stderr, width=200, word_wrap=True, extra_lines=1)
click.rich_click.USE_RICH_MARKUP = True
click.rich_click.OPTION_GROUPS = {
    "create-sequencing-mess": [
        {
            "name": "Data Options",
            "options": [
                "--samples",
                "--organisms",
                "--orgs",
                "--techs",
                "--years",
            ],
        },
        {
            "name": "Chaos Options",
            "options": [
                "--chaos",
            ],
        },
        {
            "name": "Output Options",
            "options": [
                "--outdir",
                "--seed",
                "--force",
            ],
        },
        {
            "name": "Additional Options",
            "options": [
                "--verbose",
                "--silent",
                "--version",
                "--help",
            ],
        },
    ]
}


def apply_case(text: str, case_style: str) -> str:
    """
    Apply a case style to text.

    Styles:
    - lowercase: all lowercase
    - caps: ALL UPPERCASE
    - camelcase: First Letter Of Each Part Capitalized
    - dashcase: adds a dash within numeric portions (e.g., SA001 -> sa-001)
    """
    if case_style == "lowercase":
        return text.lower()
    elif case_style == "caps":
        return text.upper()
    elif case_style == "camelcase":
        # Capitalize first letter of each segment (split by - or _)
        result = []
        capitalize_next = True
        for char in text:
            if char in "-_":
                result.append(char)
                capitalize_next = True
            elif capitalize_next:
                result.append(char.upper())
                capitalize_next = False
            else:
                result.append(char.lower())
        return "".join(result)
    elif case_style == "dashcase":
        # Add a single dash between letters and numbers (e.g., SA001 -> sa-001)
        result = []
        prev_was_letter = False
        for char in text:
            if char.isdigit() and prev_was_letter:
                result.append("-")
                prev_was_letter = False
            elif char.isalpha():
                prev_was_letter = True
            else:
                prev_was_letter = False
            result.append(char.lower())
        return "".join(result)
    return text


def get_separator(chaos_level: str, allow_mixed: bool = False) -> tuple[str, str]:
    """
    Get separators based on chaos level.

    Returns (primary_sep, secondary_sep) where:
    - low/medium: both separators are the same (either - or _)
    - high: separators can be different
    """
    if chaos_level == "high" and allow_mixed:
        return random.choice(["-", "_"]), random.choice(["-", "_"])
    else:
        sep = random.choice(["-", "_"])
        return sep, sep


def get_case_styles(chaos_level: str) -> list[str]:
    """Get available case styles based on chaos level."""
    if chaos_level == "low":
        return ["lowercase", "caps"]
    else:  # medium or high
        return ["lowercase", "caps", "camelcase", "dashcase"]


def generate_filename(
    sample_id: str,
    organism: str,
    org: str,
    year: str,
    tech: str,
    read_num: int | None,
    chaos_level: str,
) -> str:
    """
    Generate a filename based on the chaos level.

    Format: {SAMPLE_ID}-{ORGANISM}-{ORG}-{YEAR}_{TECHNOLOGY}[_R1|_R2].fastq.gz

    Chaos levels affect:
    - low: standard order, consistent separators, lowercase/caps only
    - medium: standard order, consistent separators, all case variants
    - high: shuffled order, mixed separators, all case variants
    """
    # Select case style
    case_styles = get_case_styles(chaos_level)
    case_style = random.choice(case_styles)

    # Get separators
    primary_sep, secondary_sep = get_separator(chaos_level, allow_mixed=(chaos_level == "high"))

    # Build the metadata portion
    metadata_parts = [organism, org, year]

    # Shuffle order for high chaos
    if chaos_level == "high":
        random.shuffle(metadata_parts)

    # Apply case to all parts
    sample_id_cased = apply_case(sample_id, case_style)
    metadata_cased = [apply_case(part, case_style) for part in metadata_parts]
    tech_cased = apply_case(tech, case_style)

    # Build filename
    metadata_str = primary_sep.join(metadata_cased)

    if read_num is not None:
        read_suffix = f"_R{read_num}"
        if case_style == "lowercase":
            read_suffix = read_suffix.lower()
    else:
        read_suffix = ""

    filename = f"{sample_id_cased}{primary_sep}{metadata_str}{secondary_sep}{tech_cased}{read_suffix}.fastq.gz"

    return filename


@click.command()
@click.version_option(VERSION, "--version", "-V")
@click.option(
    "--samples",
    "-s",
    default=5,
    show_default=True,
    help="Number of samples to generate",
)
@click.option(
    "--organisms",
    default=",".join(DEFAULT_ORGANISMS),
    show_default=True,
    help="Comma-separated list of organism shorthand names",
)
@click.option(
    "--orgs",
    default=",".join(DEFAULT_ORGS),
    show_default=True,
    help="Comma-separated list of organization names",
)
@click.option(
    "--techs",
    default=",".join(DEFAULT_TECHS),
    show_default=True,
    help="Comma-separated list of sequencing technologies",
)
@click.option(
    "--years",
    default=",".join(DEFAULT_YEARS),
    show_default=True,
    help="Comma-separated list of years",
)
@click.option(
    "--chaos",
    type=click.Choice(["low", "medium", "high"], case_sensitive=False),
    default="low",
    show_default=True,
    help="Level of naming chaos (low=minimal variation, high=maximum chaos)",
)
@click.option(
    "--outdir",
    "-o",
    default="./messy-reads",
    show_default=True,
    help="Directory to write the output files to",
)
@click.option(
    "--seed",
    default=42,
    show_default=True,
    help="Random seed for reproducible output",
)
@click.option("--force", is_flag=True, help="Overwrite existing output directory")
@click.option("--verbose", is_flag=True, help="Increase the verbosity of output")
@click.option("--silent", is_flag=True, help="Only critical errors will be printed")
def create_sequencing_mess(
    samples,
    organisms,
    orgs,
    techs,
    years,
    chaos,
    outdir,
    seed,
    force,
    verbose,
    silent,
):
    """
    Generate messy sequencing files for command-line training exercises.

    Creates empty .fastq.gz files with realistic naming patterns and
    configurable levels of chaos. Illumina files are paired-end (R1/R2),
    while ONT and PacBio files are single-end.

    \b
    Chaos levels:
      low    - Standard format, dashes OR underscores, lowercase OR CAPS
      medium - Standard format, dashes OR underscores, all case variants
      high   - Shuffled metadata order, mixed separators, all case variants

    \b
    Examples:
      create-sequencing-mess.py -o ./training-data
      create-sequencing-mess.py --samples 10 --chaos medium
      create-sequencing-mess.py --chaos high --samples 20 -o ./chaos
    """
    # Set random seed for reproducibility
    random.seed(seed)

    # Setup logs
    logging.basicConfig(
        format="%(asctime)s:%(name)s:%(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            RichHandler(rich_tracebacks=True, console=rich.console.Console(stderr=True))
        ],
    )
    logging.getLogger().setLevel(
        logging.ERROR if silent else logging.DEBUG if verbose else logging.INFO
    )

    # Parse comma-separated lists
    organism_list = [x.strip() for x in organisms.split(",")]
    org_list = [x.strip() for x in orgs.split(",")]
    tech_list = [x.strip().upper() for x in techs.split(",")]
    year_list = [x.strip() for x in years.split(",")]

    # Validate output directory
    outdir = Path(outdir)
    if outdir.exists():
        if force:
            logging.warning(f"Overwriting existing directory {outdir}")
            shutil.rmtree(outdir)
        else:
            logging.error(f"Output directory {outdir} already exists. Use --force to overwrite.")
            sys.exit(1)
    outdir.mkdir(parents=True, exist_ok=True)

    logging.info(f"Creating sequencing mess with chaos level: {chaos}")
    logging.info(f"Generating {samples} samples across {len(org_list)} organizations")

    # Track generated files for summary
    files_created = 0

    # Generate samples
    for i in range(1, samples + 1):
        sample_id = f"SA{i:03d}"
        organism = random.choice(organism_list)
        org = random.choice(org_list)
        year = random.choice(year_list)
        tech = random.choice(tech_list)

        # Determine if paired-end (Illumina) or single-end (ONT, PacBio)
        if tech.upper() == "ILLUMINA":
            # Generate paired-end reads with matching base filename
            base_filename = generate_filename(
                sample_id, organism, org, year, tech, 1, chaos
            )
            # Create R1 file
            filepath = outdir / base_filename
            filepath.touch()
            files_created += 1
            logging.debug(f"Created: {base_filename}")

            # Create R2 file by replacing R1 with R2 (case-sensitive replacement)
            if "_R1." in base_filename:
                r2_filename = base_filename.replace("_R1.", "_R2.")
            elif "_r1." in base_filename:
                r2_filename = base_filename.replace("_r1.", "_r2.")
            else:
                r2_filename = base_filename.replace("_R1.", "_R2.")
            filepath = outdir / r2_filename
            filepath.touch()
            files_created += 1
            logging.debug(f"Created: {r2_filename}")
        else:
            # Generate single-end read
            filename = generate_filename(
                sample_id, organism, org, year, tech, None, chaos
            )
            filepath = outdir / filename
            filepath.touch()
            files_created += 1
            logging.debug(f"Created: {filename}")

    logging.info(f"Created {files_created} files in {outdir}")
    logging.info("Mess created successfully! Time to clean it up.")


def main():
    create_sequencing_mess()


if __name__ == "__main__":
    main()
