import os


def get_threading_backend():
    if 'SOLC_THREADING_BACKEND' in os.environ:
        return os.environ['SOLC_THREADING_BACKEND']
    elif 'THREADING_BACKEND' in os.environ:
        return os.environ['THREADING_BACKEND']
    else:
        return 'stdlib'


THREADING_BACKEND = get_threading_backend()


if THREADING_BACKEND == 'stdlib':
    import subprocess
elif THREADING_BACKEND == 'gevent':
    from gevent import subprocess  # noqa: F401
else:
    raise ValueError("Unsupported threading backend.  Must be one of 'gevent' or 'stdlib'")
