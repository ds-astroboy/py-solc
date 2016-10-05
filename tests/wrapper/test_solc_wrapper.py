from __future__ import unicode_literals

import pytest

import os

from solc import get_solc_version
from solc.wrapper import (
    solc_wrapper,
)


@pytest.fixture()
def FOO_SOURCE():
    solc_version = get_solc_version()

    if solc_version in {"0.4.1", "0.4.2"}:
        return b"pragma solidity ^0.4.0;\ncontract Foo { function Foo() {} }"
    elif solc_version == "0.3.6":
        return b"contract Foo { function Foo() {} }"
    else:
        raise AssertionError("Unsupported compiler version")


@pytest.fixture()
def BAR_SOURCE():
    solc_version = get_solc_version()

    if solc_version in {"0.4.1", "0.4.2"}:
        return b"pragma solidity ^0.4.0;\ncontract Bar { function Bar() {} }"
    elif solc_version == "0.3.6":
        return b"contract Bar { function Bar() {} }"
    else:
        raise AssertionError("Unsupported compiler version")


def test_help():
    output, err, _, _ = solc_wrapper(help=True, success_return_code=1)
    assert output
    assert 'Solidity' in output
    assert not err


def test_version():
    output, err, _, _ = solc_wrapper(version=True)
    assert output
    assert 'Version' in output
    assert not err


def test_providing_stdin(FOO_SOURCE):
    output, err, _, _ = solc_wrapper(stdin_bytes=FOO_SOURCE, bin=True)
    assert output
    assert 'Foo' in output
    assert not err


def test_providing_single_source_file(contracts_dir, FOO_SOURCE):
    source_file_path = os.path.join(contracts_dir, 'Foo.sol')
    with open(source_file_path, 'wb') as source_file:
        source_file.write(FOO_SOURCE)

    output, err, _, _ = solc_wrapper(source_files=[source_file_path], bin=True)
    assert output
    assert 'Foo' in output
    assert not err


def test_providing_multiple_source_files(contracts_dir, FOO_SOURCE, BAR_SOURCE):
    source_file_a_path = os.path.join(contracts_dir, 'Foo.sol')
    source_file_b_path = os.path.join(contracts_dir, 'Bar.sol')

    with open(source_file_a_path, 'wb') as source_file:
        source_file.write(FOO_SOURCE)
    with open(source_file_b_path, 'wb') as source_file:
        source_file.write(BAR_SOURCE)

    output, err, _, _ = solc_wrapper(source_files=[source_file_a_path, source_file_b_path], bin=True)
    assert output
    assert 'Foo' in output
    assert 'Bar' in output
    assert not err
