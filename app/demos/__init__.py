"""Demo modules for AIDE Frame features."""

from . import http_call
from . import config_demo
from . import logging_demo

# Registry of available demos
DEMOS = {
    "http_call": http_call,
    "config": config_demo,
    "logging": logging_demo,
}
