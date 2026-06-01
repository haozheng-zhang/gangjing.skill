import os

from gangjing.web import run


if __name__ == "__main__":
    run(
        host=os.getenv("GANGJING_HOST", "127.0.0.1"),
        port=int(os.getenv("GANGJING_PORT", "8765")),
        open_browser=True,
    )
