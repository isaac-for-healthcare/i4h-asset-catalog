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
import importlib
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
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
        raise ValueError(f"The remote path {url_entry} is not valid")
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


def _filter_downloaded_assets(
        url_entries: List[str],
        local_dir: str, version: str | None = None,
        hash: str | None = None
    ) -> List[str]:
    """
    Filter the url_entries to only include the ones that are not downloaded.

    Args:
        url_entries: The url entries to filter.
        local_dir: The local directory to check for downloaded assets.
        version: The version of the asset.
        hash: The sha256 hash of the asset.

    Returns:
        The filtered url entries.
    """
    results = []
    # we will check if the asset is already downloaded
    for entry_url in url_entries:
        local_path = os.path.join(local_dir, get_i4h_asset_relpath(entry_url, version, hash))
        if os.path.isfile(local_path):
            print(f"Asset already downloaded to: {local_path}. Skipping download.")
        else:
            results.append(entry_url)
    return results



def _download_individual_asset(url_entry: str, download_dir: str):
    local_path = os.path.join(download_dir, get_i4h_asset_relpath(url_entry))
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    if not _is_import_ready("omni.client"):
        SimulationApp({"headless": True})
    import omni.client

    result, _, file_content = omni.client.read_file(url_entry)
    if result != omni.client.Result.OK:
        raise ValueError(f"Failed to download asset: {url_entry}")

    with open(local_path, "wb") as f:
        f.write(file_content)

    return local_path

def download_assets_local(
    url_entries: List[str],
    download_dir: str,
    concurrency: int = 2,
    timeout: float = 3600.0,
):
    """
    Download assets from url entry sources to local directory.

    Args:
        url_entries: The url entries to download.
        download_dir: The directory to download the asset to. Default is the cache directory.
        progress_callback: The callback function to call when the progress is updated.
        concurrency: The number of concurrent downloads.
        timeout: The timeout for the download.

    Returns:
        The path to the local asset.
    """

    count = 0
    total = len(url_entries)

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures_to_url = {
            executor.submit(_download_individual_asset, url_entry, download_dir): url_entry
            for url_entry in url_entries
        }

        for future in as_completed(futures_to_url, timeout=timeout):
            local_path = future.result()
            count += 1
            print(f"Downloaded {count} of {total} assets to {local_path}")


def check_local_assets(
        version: str = "0.2.0",
        download_dir: str | None = None,
        directory: str | None = None,
        hash: str | None = None,
) -> bool:
    """
    Check if the assets are already downloaded.
    """
    local_dir = get_i4h_local_asset_path(version, download_dir, hash)
    paths = list_i4h_asset_url(get_i4h_asset_path(version, hash, directory))
    return len(_filter_downloaded_assets(paths, local_dir, version, hash)) == len(paths)



def retrieve_asset(
    version: str = "0.2.0",
    download_dir: str | None = None,
    child_path: str | None = None,
    hash: str | None = None,
    force_download: bool = False
) -> str:
    """
    Download the asset from the remote path to the download directory.

    Args:
        version: The version of the asset to download.
        download_dir: The directory to download the asset to.
        child_path: The child path of the asset to download.
        hash: The sha256 hash of the asset.
        force_download: If True, the asset will be downloaded even if it already exists.

    Returns:
        The path to the local asset.
    """
    local_dir = get_i4h_local_asset_path(version, download_dir, hash)
    remote_path = get_i4h_asset_path(version, hash)

    if child_path is not None:
        remote_path = os.path.join(remote_path, child_path)

    paths = list_i4h_asset_url(remote_path)
    if force_download:
        url_entries = paths
    else:
        url_entries = _filter_downloaded_assets(paths, local_dir, version, hash)

    download_assets_local(url_entries, local_dir)
    return local_dir
