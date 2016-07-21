from __future__ import absolute_import

import subprocess
import textwrap

from .exceptions import (
    CompileError,
)
from .utils.string import (
    coerce_return_to_text,
)


SOLC_BINARY = 'solc'


@coerce_return_to_text
def solc_wrapper(solc_binary=SOLC_BINARY,
                 stdin_bytes=None,
                 help=None,
                 version=None,
                 add_std=None,
                 combined_json=None,
                 optimize=None,
                 optimize_runs=None,
                 libraries=None,
                 output_dir=None,
                 gas=None,
                 assemble=None,
                 link=None,
                 source_files=None,
                 ast=None,
                 ast_json=None,
                 asm=None,
                 asm_json=None,
                 opcodes=None,
                 bin=None,
                 bin_runtime=None,
                 clone_bin=None,
                 abi=None,
                 interface=None,
                 hashes=None,
                 userdoc=None,
                 devdoc=None,
                 formal=None,
                 success_return_code=0):
    command = ['solc']

    if help:
        command.append('--help')

    if version:
        command.append('--version')

    if add_std:
        command.append('--add-std')

    if optimize:
        command.append('--optimize')

    if optimize_runs is not None:
        command.extend(('--optimize-runs', str(optimize_runs)))

    if link:
        command.append('--link')

    if libraries is not None:
        command.extend(('--libraries', libraries))

    if output_dir is not None:
        command.extend(('--output-dir', output_dir))

    if combined_json:
        command.extend(('--combined-json', combined_json))

    if gas:
        command.append('--gas')

    if assemble:
        command.append('--assemble')

    if source_files is not None:
        command.extend(source_files)

    #
    # Output configuration
    #
    if ast:
        command.append('--ast')

    if ast_json:
        command.append('--ast-json')

    if asm:
        command.append('--asm')

    if asm_json:
        command.append('--asm-json')

    if opcodes:
        command.append('--opcodes')

    if bin:
        command.append('--bin')

    if bin_runtime:
        command.append('--bin-runtime')

    if clone_bin:
        command.append('--clone-bin')

    if abi:
        command.append('--abi')

    if interface:
        command.append('--interface')

    if hashes:
        command.append('--hashes')

    if userdoc:
        command.append('--userdoc')

    if devdoc:
        command.append('--devdoc')

    if formal:
        command.append('--formal')

    if stdin_bytes is not None:
        stdin = subprocess.Popen(['echo', stdin_bytes], stdout=subprocess.PIPE).stdout
    else:
        stdin = subprocess.PIPE

    proc = subprocess.Popen(command,
                            stdin=stdin,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    stdoutdata, stderrdata = proc.communicate()

    if proc.returncode != success_return_code:
        error_message = textwrap.dedent(("""
        Compilation Failed
        > command: `{command}`
        > return code: `{return_code}`
        > stderr:
        {stderrdata}
        > stdout:
        {stdoutdata}
        """).format(
            command=' '.join(command),
            return_code=proc.returncode,
            stderrdata=stderrdata,
            stdoutdata=stdoutdata,
        )).strip()
        raise CompileError(error_message)

    return stdoutdata, stderrdata
