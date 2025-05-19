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

import asyncio
import json
import os
import shutil
import tempfile
import zipfile
import importlib
import sys

from typing import List
from isaacsim import SimulationApp

__all__ = [
    "get_i4h_asset_hash",
    "get_i4h_asset_path",
    "get_i4h_local_asset_path",
    "retrieve_asset",
]

_I4H_ASSET_ROOT = {
    "dev": "https://isaac-dev.ov.nvidia.com/omni/web3/omniverse://isaac-dev.ov.nvidia.com/Library/IsaacHealthcare",
    "staging": "https://omniverse-content-staging.s3-us-west-2.amazonaws.com/Assets/Isaac/Healthcare",
    "production": "https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/Healthcare"
}

_DEFAULT_DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), ".cache", "i4h-assets")


def _is_import_ready(package_name: str):
    """
    Check if we need to start the simulation app to import the package. If it does, it will return True.
    """
    # try if the package is already imported
    if package_name in sys.modules:
        return True

    try:
        importlib.import_module(package_name)
    except ImportError:
        return False
    return True

    
def _get_configuration() -> str:
    """Get the current configuration of the asset root."""
    return os.environ.get("I4H_ASSET_ENV", "dev")


def _set_configuration(config: str):
    """Set the current configuration of the asset root for internal tests."""
    if config not in _I4H_ASSET_ROOT:
        raise ValueError(f"Invalid configuration: {config}")
    os.environ["I4H_ASSET_ENV"] = config


def get_i4h_asset_hash(version: str = "0.2.0") -> str:
    """Get the sha256 hash for the given version."""
    # Get it from the environment variable if it exists
    if os.environ.get("ISAAC_ASSET_SHA256_HASH"):
        return os.environ.get("ISAAC_ASSET_SHA256_HASH")
    # Otherwise, get it from the file
    with open(os.path.join(os.path.dirname(__file__), "assets_sha256.json"), "r") as f:
        return json.load(f).get(version, None)


def get_i4h_asset_path(version: str = "0.2.0", hash: str | None = None) -> str:
    """
    Get the path to the i4h asset for the given version.

    Args:
        version: The version of the asset to get.
        hash: The sha256 hash of the asset.

    Returns:
        The path to the i4h asset.
    """
    asset_root = _I4H_ASSET_ROOT.get(_get_configuration())
    if hash is None:
        hash = get_i4h_asset_hash(version=version)
    remote_path = f"{asset_root}/{version}/{hash}"

    return remote_path


def get_i4h_local_asset_path(
        version: str = "0.2.0",
        download_dir: str | None = None,
        hash: str | None = None
    ) -> str:
    """
    Get the path to the i4h asset for the given version.

    Args:
        version: The version of the asset to get.
        download_dir: The directory to download the asset to.
        hash: The sha256 hash of the asset.

    Returns:
        The path to the local asset.
    """
    if download_dir is None:
        download_dir = _DEFAULT_DOWNLOAD_DIR
    if hash is None:
        hash = get_i4h_asset_hash(version=version)
    return os.path.join(download_dir, hash)


def get_i4h_asset_relpath(url_entry: str, version: str = "0.2.0", hash: str | None = None) -> str:
    """
    Get relative path of the item specified by the url_entry should be located in the local asset directory.

    Args:
        url_entry: The entry of the item
        version: The version of the asset
        hash: The sha256 hash of the asset
    
    Returns:
        The relative path of the item.
    """
    asset_root = get_i4h_asset_path(version, hash)
    if _get_configuration() == "dev":
        asset_root = asset_root.replace("https://isaac-dev.ov.nvidia.com/omni/web3/", "")

    if not url_entry.startswith(asset_root):
        raise ValueError(f"URL entry {url_entry} expects to begin with {asset_root}")
    
    return os.path.relpath(url_entry, asset_root)


def _is_url_folder(url_entry: str) -> bool:
    """Check if the url_entry is a folder."""
    # This is an internal function
    # So we don't expect users to call this without the simulation app
    if not _is_import_ready("omni.client"):
        SimulationApp({"headless": True})
    import omni.client
    result, entries = omni.client.stat(url_entry)
    if result != omni.client.Result.OK:
        raise ValueError(f"Failed to check if {url_entry} is a folder")
    return entries.size == 0


def list_i4h_asset_url(url_entry: str) -> List[str]:
    """
    List all the items in the url_entry. When it is a folder, it will return all the items in the folder.
    When it is a file, it will return a list with the file itself.
    """
    if not _is_import_ready("isaacsim.storage.native.nucleus"):
        SimulationApp({"headless": True})
    from isaacsim.storage.native.nucleus import _list_files
    if not _is_url_folder(url_entry):
        return [url_entry]

    # _list_files is an async function
    _, entries = asyncio.run(_list_files(url_entry))
    return entries


def retrieve_asset(
    version: str = "0.2.0",
    download_dir: str | None = None,
    hash: str | None = None,
    force_download: bool = False
) -> str:
    """
    Download the asset from the remote path to the download directory.

    Args:
        version: The version of the asset to download.
        download_dir: The directory to download the asset to.
        hash: The sha256 hash of the asset.
        force_download: If True, the asset will be downloaded even if it already exists.

    Returns:
        The path to the local asset.
    """
    local_path = get_i4h_local_asset_path(version, download_dir, hash)

    # If the asset hash is a folder in download_dir and is not empty, skip the download
    if os.path.exists(local_path) and len(os.listdir(local_path)) > 0 and not force_download:
        print(f"Assets already downloaded to: {local_path}")
        return local_path

    # Force download or the folder is empty
    if os.path.isdir(local_path):
        shutil.rmtree(local_path)

    if not _is_import_ready("omni.client"):
        SimulationApp({"headless": True})
    import omni.client
    
    remote_path = get_i4h_asset_path(version, hash)
    result, _, file_content = omni.client.read_file(remote_path)

    if result != omni.client.Result.OK:
        raise ValueError(f"Failed to download asset: {remote_path}")

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            with open(os.path.join(temp_dir, f"i4h-assets-v{version}.zip"), "wb") as f:
                f.write(file_content)
            # TODO: Check sha256 hash
            with zipfile.ZipFile(os.path.join(temp_dir, f"i4h-assets-v{version}.zip"), "r") as zip_ref:
                os.makedirs(local_path, exist_ok=True)
                zip_ref.extractall(local_path)
                print(f"Assets downloaded to: {local_path}")
            return local_path
    except Exception as e:
        raise ValueError(f"Failed to extract asset: {remote_path}") from e
