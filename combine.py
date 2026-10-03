"""Combine MFA-aligned TextGrids with selected tiers from the original TextGrids.

The output TextGrid contains, in this order:
  1. "phones"  - from the MFA output
  2. "words"   - from the MFA output
  3. every tier named in `keep_tiers`, copied from the ORIGINAL TextGrid

Any other tier in the original file (e.g. the IPA tier) is ignored.

Usage:
    python3 combine.py ./alignedData/ /path/to/original/ --keep Sentence Speaker
"""

import copy
import logging
import os
import sys
import traceback

import textgrids

# Used when the caller doesn't say which tiers to keep. posTag.py needs "Sentence".
DEFAULT_KEEP_TIERS = ["Sentence"]

# Names the combined file uses for the MFA tiers (posTag.py expects "words").
PHONES_NAME = "phones"
WORDS_NAME = "words"

log = logging.getLogger("combine")

class CombineError(Exception):
    """Raised when a single file cannot be combined."""

def find_mfa_tier(grid, kind):
    """Return the name of the MFA tier of the given kind ("words" or "phones").

    MFA names tiers "words"/"phones" for a single speaker and
    "<speaker> - words"/"<speaker> - phones" otherwise; both are handled.
    """
    names = list(grid.keys())
    for name in names:
        if name.lower() == kind:
            return name
    for name in names:
        if name.lower().endswith(" - " + kind):
            return name
    raise CombineError(f"no '{kind}' tier in MFA output (tiers found: {names})")

def resolve_tier(grid, requested):
    """Find `requested` in `grid`, preferring an exact match, then ignoring case.

    Returns the tier's actual name in the grid, or None if it isn't there.
    """
    if requested in grid:
        return requested
    lowered = {name.lower(): name for name in grid.keys()}
    return lowered.get(requested.lower())

def combine_tiers(mfa_file, original_file, out_file, keep_tiers=None):
    """Write `out_file` containing MFA phones/words plus `keep_tiers` from the original.

    Returns the list of tier names written, in order.
    Raises CombineError if the MFA tiers are missing. A requested tier that is
    missing from the original is logged as a warning and skipped.
    """
    if keep_tiers is None:
        keep_tiers = DEFAULT_KEEP_TIERS

    mfa_grid = textgrids.TextGrid(mfa_file)
    original_grid = textgrids.TextGrid(original_file)

    out_grid = textgrids.TextGrid()
    out_grid.xmin = mfa_grid.xmin
    out_grid.xmax = mfa_grid.xmax

    out_grid[PHONES_NAME] = copy.deepcopy(mfa_grid[find_mfa_tier(mfa_grid, "phones")])
    out_grid[WORDS_NAME] = copy.deepcopy(mfa_grid[find_mfa_tier(mfa_grid, "words")])

    if abs(original_grid.xmax - mfa_grid.xmax) > 0.01:
        log.warning(
            "%s: duration differs between original (%.3fs) and MFA output (%.3fs)",
            os.path.basename(original_file), original_grid.xmax, mfa_grid.xmax,
        )

    for requested in keep_tiers:
        actual = resolve_tier(original_grid, requested)
        if actual is None:
            log.warning(
                "%s: tier '%s' not found (available: %s)",
                os.path.basename(original_file), requested, list(original_grid.keys()),
            )
            continue
        if actual in out_grid:
            log.warning(
                "%s: tier '%s' collides with an MFA tier name and was skipped",
                os.path.basename(original_file), actual,
            )
            continue
        out_grid[actual] = copy.deepcopy(original_grid[actual])

    out_grid.write(out_file)
    return list(out_grid.keys())

def main(aligned, original, keep_tiers=None, out_dir="./temp/"):
    """Combine every aligned .TextGrid in `aligned` with its match in `original`.

    Returns (succeeded, failed, skipped) as lists of file names.
    """
    os.makedirs(out_dir, exist_ok=True)
    succeeded, failed, skipped = [], [], []

    for file_name in sorted(os.listdir(aligned)):
        if not file_name.endswith(".TextGrid"):
            continue

        original_file = os.path.join(original, file_name)
        if not os.path.exists(original_file):
            log.warning("%s: no matching original TextGrid, skipping", file_name)
            skipped.append(file_name)
            continue

        try:
            combine_tiers(
                os.path.join(aligned, file_name),
                original_file,
                os.path.join(out_dir, file_name),
                keep_tiers,
            )
            succeeded.append(file_name)
        except Exception as error:  # one bad file shouldn't stop the batch
            log.error("%s: could not combine (%s)", file_name, error)
            log.debug(traceback.format_exc())
            failed.append(file_name)

    log.info(
        "Combine finished: %d succeeded, %d failed, %d skipped",
        len(succeeded), len(failed), len(skipped),
    )
    return succeeded, failed, skipped

def _setup_logging(log_file, verbose):
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file, mode="a", encoding="utf-8"))
        logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
        handlers=handlers,
    )

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Combine MFA-aligned TextGrids with selected tiers from the originals.")
    parser.add_argument("alignedPath", help="folder of MFA-aligned TextGrids")
    parser.add_argument("originalPath", help="folder of original TextGrids")
    parser.add_argument("--keep", nargs="+", default=DEFAULT_KEEP_TIERS, metavar="TIER", help="original tiers to keep (default: %(default)s). Matching ignores case.",)
    parser.add_argument("--out", default="./temp/", help="output folder (default: %(default)s)")
    parser.add_argument("--log", default="combine_log.txt", help="log file (appended to)")
    parser.add_argument("-v", "--verbose", action="store_true", help="show tracebacks")
    args = parser.parse_args()

    _setup_logging(args.log, args.verbose)
    _, failed_files, _ = main(args.alignedPath, args.originalPath, args.keep, args.out)
    sys.exit(1 if failed_files else 0)