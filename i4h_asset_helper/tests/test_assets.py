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
import tempfile
import pytest

from i4h_asset_helper import BaseI4HAssets, get_i4h_asset_hash, get_i4h_asset_path, get_i4h_local_asset_path, retrieve_asset
from i4h_asset_helper.assets import _I4H_ASSET_ROOT
from isaacsim import SimulationApp

VERSIONS = ["0.1.0", "0.2.0"]
SimulationApp({"headless": True})


def test_get_i4h_asset_path_valid_version():
    # Test with valid version
    result = get_i4h_asset_path()
    hash = get_i4h_asset_hash()
    version = VERSIONS[1]
    expected_production_path = f"{_I4H_ASSET_ROOT['production']}/{version}/{hash}"
    expected_staging_path = f"{_I4H_ASSET_ROOT['staging']}/{version}/{hash}"
    expected_dev_path = f"{_I4H_ASSET_ROOT['dev']}/{version}/{hash}"
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


def test_get_i4h_local_asset_path_override():
    os.environ["I4H_ASSET_DOWNLOAD_DIR"] = "/tmp/i4h-assets"
    result = get_i4h_local_asset_path()
    expected_path = os.path.join("/tmp/i4h-assets", get_i4h_asset_hash())
    assert result == expected_path
    os.environ.pop("I4H_ASSET_DOWNLOAD_DIR")


def test_set_env_var_hash():
    os.environ["ISAAC_ASSET_SHA256_HASH"] = "test_hash"
    assert get_i4h_asset_hash() == "test_hash"
    os.environ.pop("ISAAC_ASSET_SHA256_HASH")


def test_set_env_var_root():
    os.environ["I4H_ASSET_ENV"] = "dev"
    assert get_i4h_asset_path().startswith(_I4H_ASSET_ROOT["dev"])
    os.environ.pop("I4H_ASSET_ENV")


def test_retrieve_asset():
    with tempfile.TemporaryDirectory() as temp_dir:
        local_dir = retrieve_asset(download_dir=temp_dir, child_path="Test")
        hash = get_i4h_asset_hash()
        assert hash in local_dir
        assert os.path.exists(os.path.join(local_dir, "Test"))


def test_class_inheritance():
    class TestI4HAssets(BaseI4HAssets):
        test = "Test/basic.usda"

    with tempfile.TemporaryDirectory() as temp_dir:
        test_assets = TestI4HAssets(download_dir=temp_dir)
        # resource will be downloaded automatically
        local_usda = test_assets.test
        hash = get_i4h_asset_hash()
        assert os.path.exists(local_usda)
        assert hash in local_usda

