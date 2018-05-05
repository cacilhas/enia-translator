import os.path as path
from vcr import VCR

vcr = VCR(
    cassette_library_dir=path.realpath(path.join(
        path.dirname(__file__), 'cassettes',
    ))
)
