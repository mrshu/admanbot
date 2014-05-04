#!/usr/bin/env python
import os

from brutal.core.management import exec_overlord

if __name__ == "__main__":
    os.environ.setdefault("BRUTAL_CONFIG_MODULE", "admanbot.config")
    exec_overlord("admanbot.config")