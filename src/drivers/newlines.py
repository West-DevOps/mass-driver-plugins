import os
import pathlib
import logging

from mass_driver.models.patchdriver import PatchDriver, PatchResult, PatchOutcome
from mass_driver.models.repository import ClonedRepo


class NewLineDriver(PatchDriver):
    """Adds newlines to all files which do not have an empty newline at EOF marker."""

    @staticmethod
    def put_newlines_in_files(directory: pathlib.Path) -> tuple[int, int]:
        """
        Puts newlines into files that need them to get rid of the annoying 'no newline at EOF' message git throws down
        when you are reviewing PRs

        Args:
            directory: Directory to work on (the root of the repo)

        Returns:
            (fixed_files, failed_reads)
        """
        fixed_files = 0
        failed_reads = 0

        for entry in os.listdir(directory):
            full_path = os.path.join(directory, entry)
            if os.path.isdir(full_path):
                # Get recursing!
                r = NewLineDriver.put_newlines_in_files(pathlib.Path(full_path))
                fixed_files += r[0]
                failed_reads += r[1]
            else:
                with open(full_path, 'r') as reader:
                    try:
                        content = reader.read()
                    except UnicodeDecodeError as e:
                        logging.debug(f"{e} caught working on file {full_path} (it's not a regular text file)")
                        failed_reads += 1
                        continue

                    if len(content) == 0:
                        # Just an empty file, moving on...
                        continue

                    if content[len(content)-1:len(content)] != '\n':
                        logging.debug(f"Found file with no newline: {full_path}")
                        with open(full_path, 'a') as writer:
                            writer.write('\n')
                        fixed_files += 1

        return fixed_files, failed_reads

    def run(self, repo: ClonedRepo) -> PatchResult:
        """
        Main migration/driver function.  Just calls the recursive function `put_newlines_in_files`
        Args:
            repo: ClonedRepo object from the source run.

        Returns:
            Result of patching
        """
        files_newlined, failed_reads = NewLineDriver.put_newlines_in_files(pathlib.Path(repo.cloned_path))

        if files_newlined > 0:
            return PatchResult(outcome=PatchOutcome.PATCHED_OK,
                               details=f"{files_newlined} files had newlines added,"
                                       f"{failed_reads} files failed to be decoded.")
        elif files_newlined == 0:
            return PatchResult(outcome=PatchOutcome.PATCH_DOES_NOT_APPLY,
                               details="No files needed newlines putting in")
        else:
            return PatchResult(outcome=PatchOutcome.PATCH_ERROR, details=f"Something strange happened..."
                                                                         f"Failed read count: {failed_reads}")
