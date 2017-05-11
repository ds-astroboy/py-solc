import os

import pytest

from solc import (
    compile_files,
    compile_standard,
)

from solc.exceptions import ContractsNotFound
from ..test_utils import skipif_no_standard_json


def test_compile_empty_folder():
    """Execute compile on a folder without contracts."""

    with pytest.raises(ContractsNotFound):
        compile_files([])


@skipif_no_standard_json
def test_compile_standard_empty_sources():
	with pytest.raises(ContractsNotFound):
		compile_standard({'language': 'Solidity', 'sources': {}})
