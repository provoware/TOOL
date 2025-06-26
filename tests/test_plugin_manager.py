from plugin_manager import scan_and_load


def test_scan_no_plugins(tmp_path):
    # Should not raise even if plugin directory empty
    scan_and_load(gui=None)
