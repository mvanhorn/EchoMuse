"""SRV target shared by the controller's mDNS advertisements."""

import os


def service_target(default_name: str) -> str:
    # Host networking does not expose the Docker host's hostname.
    name = os.environ.get("MDNS_HOSTNAME", "").strip().rstrip(".")
    if name.lower().endswith(".local"):
        name = name[:-6]
    return f"{name or default_name}.local."
