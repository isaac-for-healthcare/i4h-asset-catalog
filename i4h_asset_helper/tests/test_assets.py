# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import pytest

from i4h_asset_helper import get_i4h_asset_path, get_i4h_local_asset_path
from i4h_asset_helper.assets import _I4H_ASSET_ROOT, _get_sha256_hash


def test_get_i4h_asset_path_valid_version():
    # Test with valid version
    result = get_i4h_asset_path(version="0.1")
    hash = _get_sha256_hash()["0.1"]
    expected_path = f"{_I4H_ASSET_ROOT['dev']}/Library/IsaacHealthcare/0.1/i4h-assets-v0.1-{hash}.zip"
    assert result == expected_path

def test_get_i4h_asset_path_invalid_version():
    # Test with invalid version
    with pytest.raises(ValueError, match="Invalid version"):
        get_i4h_asset_path(version="invalid")

def test_get_i4h_local_asset_path():
    result = get_i4h_local_asset_path(version="0.1")
    expected_path = os.path.join(os.path.expanduser("~"), ".cache", "i4h-assets", _get_sha256_hash()["0.1"])
    assert result == expected_path
