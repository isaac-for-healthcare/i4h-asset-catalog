import os

import pytest

from i4h_asset_helper import get_i4h_asset_path, get_i4h_local_asset_path
from i4h_asset_helper.assets import _I4H_ASSET_ROOT, _get_sha256_hash


def test_get_i4h_asset_path_valid_version():
    # Test with valid version
    result = get_i4h_asset_path(version="0.1")
    hash = _get_sha256_hash()["0.1"]
    expected_path = f"{_I4H_ASSET_ROOT['nucleus']}/Library/IsaacHealthcare/0.1/i4h-assets-v0.1-{hash}.zip"
    assert result == expected_path

def test_get_i4h_asset_path_invalid_version():
    # Test with invalid version
    with pytest.raises(ValueError, match="Invalid version"):
        get_i4h_asset_path(version="invalid")

def test_get_i4h_local_asset_path():
    result = get_i4h_local_asset_path(version="0.1")
    expected_path = os.path.join(os.path.expanduser("~"), ".cache", "i4h-assets", _get_sha256_hash()["0.1"])
    assert result == expected_path
