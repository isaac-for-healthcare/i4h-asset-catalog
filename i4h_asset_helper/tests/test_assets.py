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

from i4h_asset_helper.assets import (
    get_i4h_asset_hash,
    get_i4h_asset_path,
    get_i4h_local_asset_path,
    _I4H_ASSET_ROOT,
)

VERSIONS = ["0.1.0", "0.2.0"]


def test_get_i4h_asset_path_valid_version():
    # Test with valid version
    result = get_i4h_asset_path()
    hash = get_i4h_asset_hash()
    version = VERSIONS[1]
    expected_production_path = f"{_I4H_ASSET_ROOT['production']}/{version}/i4h-assets-v{version}-{hash}.zip"
    expected_staging_path = f"{_I4H_ASSET_ROOT['staging']}/{version}/i4h-assets-v{version}-{hash}.zip"
    expected_dev_path = f"{_I4H_ASSET_ROOT['dev']}/{version}/i4h-assets-v{version}-{hash}.zip"
    expected_paths = {expected_staging_path, expected_dev_path, expected_production_path}
    assert result in expected_paths


def test_get_i4h_asset_path_invalid_version():
    # Test with invalid version
    with pytest.raises(ValueError, match="Invalid version"):
        get_i4h_asset_path(version="invalid")


def test_get_i4h_local_asset_path():
    result = get_i4h_local_asset_path()
    expected_path = os.path.join(os.path.expanduser("~"), ".cache", "i4h-assets", get_i4h_asset_hash())
    assert result == expected_path


def test_set_env_var_hash():
    os.environ["ISAAC_ASSET_SHA256_HASH"] = "test_hash"
    assert get_i4h_asset_hash() == "test_hash"
    os.environ.pop("ISAAC_ASSET_SHA256_HASH")


def test_set_env_var_root():
    os.environ["I4H_ASSET_ENV"] = "dev"
    assert get_i4h_asset_path().startswith(_I4H_ASSET_ROOT["dev"])
    os.environ.pop("I4H_ASSET_ENV")
