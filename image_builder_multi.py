#!/usr/bin/env python3

import argparse
from pathlib import Path

import yaml

from image_builder import build_an_image

SCRIPT_DIR = Path(__file__).resolve().parent
LOGS_DIR = SCRIPT_DIR / "logs"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        required=False,
        help="If passed, the path to the simplestreams repository",
    )
    parser.add_argument("-c", "--config", type=Path, required=True, help="The config")
    args = parser.parse_args()

    config = yaml.safe_load(args.config.open("r", encoding="utf-8"))
    returncode = 0

    jobs: list[tuple[str, str, str]] = [
        (debian, distro, variant)
        for debian, distros in config["jobs"].items()
        for distro, variants in distros.items()
        for variant in variants
    ]

    for debian, distro, variant in jobs:
        print(f"############### Building {debian} {distro} {variant}...")
        logfile = LOGS_DIR / f"{debian}_{distro}_{variant}.log"
        try:
            build_an_image(debian, distro, variant, logfile, args.output)
        except Exception:
            print(f"Could not build image {debian} {distro} {variant}!")
            returncode = 1

    exit(returncode)


if __name__ == "__main__":
    main()
