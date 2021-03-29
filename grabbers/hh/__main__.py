import argparse

from aiohttp.web import run_app
from aiomisc import bind_socket
from aiomisc.log import (
    LogFormat,
    LogLevel,
    basic_config,
)
from configargparse import ArgumentParser  # type: ignore

from grabbers.hh.app import create_app


ENV_VAR_PREFIX = "GRABS_"


parser = ArgumentParser(
    auto_env_var_prefix=ENV_VAR_PREFIX, allow_abbrev=False, formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
group = parser.add_argument_group("Logging options")
group.add_argument("--log-level", default=LogLevel.info, choices=("debug", "info", "warning", "error", "fatal"))
group.add_argument("--log-format", choices=LogFormat.choices(), default="color")


if __name__ == "__main__":
    args = parser.parse_args()

    basic_config(args.log_level, args.log_format, buffered=True)

    sock = bind_socket(address="127.0.0.1", port=8888, proto_name="http")

    app = create_app()
    run_app(app, sock=sock)
