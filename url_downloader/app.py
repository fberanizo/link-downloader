# -*- coding: utf-8 -*-
"""ASGI server."""
import argparse
import io
import sys
from typing import Optional

import uvicorn
import requests
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from url_downloader import __version__

app = FastAPI(
    title="URL Downloader",
    description="A didatic API that downloads the contents returned by url.",
    version=__version__,
)


@app.get("/v1", response_class=StreamingResponse)
async def in_memory(url: Optional[str]):
    """
    Handles GET requests to /v1.

    Parameters
    ----------
    url : str or None

    Returns
    -------
    StreamingResponse
    """
    # Performs download and store in-memory
    contents = b""
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=8192):
            contents += chunk

    # Pass the whole content to BytesIO
    bytes_io = io.BytesIO(contents)

    filename = url.split("/")[-1]
    response = StreamingResponse(bytes_io, media_type="application/x-zip-compressed")
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response


@app.get("/v2", response_class=StreamingResponse)
async def generator(url: Optional[str]):
    """
    Handles GET requests to /v2.

    Parameters
    ----------
    url : str or None

    Returns
    -------
    StreamingResponse
    """
    # Makes a generator to perform lazy evaluation
    def generator(url):
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=8192):
                yield chunk

    # Lazily pass the content
    contents = generator(url)

    filename = url.split("/")[-1]
    response = StreamingResponse(contents, media_type="application/x-zip-compressed")
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response


@app.get("/v3", response_class=StreamingResponse)
async def rawio_base(url: Optional[str]):
    """
    Handles GET requests to /v3.

    Parameters
    ----------
    url : str or None

    Returns
    -------
    StreamingResponse
    """
    # Makes a reader
    class Downloader(io.RawIOBase):

        def __init__(self, url):
            io.RawIOBase.__init__(self)

            self.r = requests.get(url, stream=True)
            self.r.raise_for_status()
            self.iterator = None

        def read(self, size=-1):
            if self.iterator is None:
                self.iterator = self.r.iter_content(chunk_size=size)
            return next(self.iterator)

    # Lazily pass the content to BytesIO
    downloader = Downloader(url)

    filename = url.split("/")[-1]
    response = StreamingResponse(downloader, media_type="application/x-zip-compressed")
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response


def parse_args(args):
    """Takes argv and parses API options."""
    parser = argparse.ArgumentParser(
        description="URL Downloader API",
    )
    parser.add_argument(
        "--host", type=str, default="127.0.0.1", help="Host for HTTP server (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="Port for HTTP server (default: 8000)",
    )
    return parser.parse_args(args)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])

    uvicorn.run(app, host=args.host, port=args.port)
