import socket

import pytest

import _oww_stub

_oww_stub.install()

import em_ble_proxy
import em_controller
import em_esphome


@pytest.mark.parametrize("hostname", ["music", "music.local.", ""])
def test_service_targets(monkeypatch, hostname):
    monkeypatch.setenv("MDNS_HOSTNAME", hostname)
    monkeypatch.setattr(socket, "gethostname", lambda: "container-id")
    device = "aabbccddeeff"
    monkeypatch.setattr(em_esphome, "_serialno_to_mac", lambda _: "aa:bb:cc:dd:ee:ff")
    controller = em_controller._make_mdns_info(False)
    voice = em_esphome._make_device_mdns_info(device, "Kitchen", 6053, device)
    proxy = em_ble_proxy._make_mdns_info(device, "Kitchen", 6054)

    for info, name, port in (
        (controller, em_controller.MDNS_NAME, em_controller.SERVER_PORT),
        (voice, f"echomuse-{device}", 6053),
        (proxy, f"echomuse-{device}-bt", 6054),
    ):
        assert info.server == ("music.local." if hostname else f"{name}.local.")
        assert info.name == f"{name}.{info.type}"
        assert info.port == port
    assert voice.properties[b"mac"] == device.encode()
    assert proxy.properties[b"mac"] == b"a8bbccddeeff"
