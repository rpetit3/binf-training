#! /usr/bin/env python3
import logging
import os
import random
import shutil
import sys

from pathlib import Path

import rich
import rich.console
import rich.traceback
import rich_click as click
from rich.logging import RichHandler

VERSION = "0.0.1"

def misspell_word(word):
    """
    Introduces a single, random misspelling into a given word.
    Possible errors: deletion, insertion, substitution, or transposition.
    """
    if not word:
        return ""

    error_type = random.choice(["delete", "insert", "substitute"])
    word_list = list(word)
    index = random.randint(0, len(word_list) - 1)

    if error_type == "delete" and len(word_list) > 1:
        del word_list[index]
    elif error_type == "insert":
        random_char = random.choice("abcdefghijklmnopqrstuvwxyz")
        word_list.insert(index, random_char)
    elif error_type == "substitute":
        random_char = random.choice("abcdefghijklmnopqrstuvwxyz")
        word_list[index] = random_char
    elif error_type == "transpose" and len(word_list) > 1 and index < len(word_list) - 1:
        word_list[index], word_list[index + 1] = word_list[index + 1], word_list[index]

    return "".join(word_list)

# Set up Rich
stderr = rich.console.Console(stderr=True)
rich.traceback.install(console=stderr, width=200, word_wrap=True, extra_lines=1)
click.rich_click.USE_RICH_MARKUP = True
click.rich_click.OPTION_GROUPS = {
    "clean-the-house": [
        {
            "name": "Options",
            "options": [
                "--outdir",
                "--messy",
                "--messier",
                "--messiest",
            ],
        },
        {
            "name": "Additional Options",
            "options": [
                "--force",
                "--verbose",
                "--silent",
                "--version",
                "--help",
            ],
        },
    ]
}

@click.command()
@click.version_option(VERSION, "--version", "-V")
@click.option(
    "--outdir",
    "-o",
    default="./clean-the-house",
    show_default=True,
    help="Directory to write the output files to",
)
@click.option("--messy", is_flag=True, help="Create a messy house")
@click.option("--messier", is_flag=True, help="Create a messier house")
@click.option("--messiest", is_flag=True, help="Create the messiest house")
@click.option("--force", is_flag=True, help="Overwrite existing files")
@click.option("--verbose", is_flag=True, help="Increase the verbosity of output")
@click.option("--silent", is_flag=True, help="Only critical errors will be printed")
def clean_the_house(
    outdir,
    messy,
    messier,
    messiest,
    force,
    verbose,
    silent,
):
    """A command-line tool to generate a messy house that needs cleaning."""
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

    # If outdir does not exist, create it
    outdir = Path(outdir)
    if outdir.exists():
        if force:
            logging.warning(f"Overwriting existing directory {outdir}")
            shutil.rmtree(outdir)
        else:
            logging.error(f"Output directory {outdir} already exists. Use --force to overwrite.")
            sys.exit(1)
    outdir.mkdir(parents=True, exist_ok=True)

    # Begin creating a messy house
    messy_level = sum([bool(messy), bool(messier)*2, bool(messiest)*3])
    logging.info(f"Starting to create a messy ({messy_level}) house...")
    rooms = ["living_room", "kitchen", "bedroom", "bathroom", "garage"]
    items = ["sofa", "lamp", "table", "clothes", "toys", "books", "plates", "pans", "food",
             "trash", "toothbrush", "shampoo", "tools", "car-parts"]

    logging.info(f"Creating rooms")
    for room in rooms:
        room_dir = f"{outdir}/{room}"
        os.makedirs(room_dir, exist_ok=True)

    logging.info(f"Creating a mess")
    for item in items:
        for i in range(random.randint(50, 100)):
            this_item = item
            if random.random() < (0.3 * messy_level):
                this_item = misspell_word(this_item)
            item_file = f"{outdir}/{this_item}_{i:03}.txt"

            with open(item_file, "w") as f:
                if random.random() < (0.1 * messy_level):
                    f.write(f"Please remove this item from the house.\n")
                f.write(f"Please keep this item\n")
    logging.info("Finished creating a messy house.")


def main():
    clean_the_house()


if __name__ == "__main__":
    main()
