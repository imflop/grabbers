import asyncio

from grabbers.hh.app import run


if __name__ == "__main__":
    asyncio.run(run("Remote"), debug=True)
