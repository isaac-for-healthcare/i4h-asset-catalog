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

import json
import os
import shutil
import tempfile
import zipfile

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


def get_i4h_asset_hash(version: str = "0.1.0") -> str:
    """Get the sha256 hash for the given version."""
    # Get it from the environment variable if it exists
    if os.environ.get("ISAAC_ASSET_SHA256_HASH"):
        return os.environ.get("ISAAC_ASSET_SHA256_HASH")
    # Otherwise, get it from the file
    with open(os.path.join(os.path.dirname(__file__), "assets_sha256.json"), "r") as f:
        return json.load(f).get(version, None)


def get_i4h_asset_path(version: str = "0.1.0", hash: str | None = None) -> str:
    """
    Get the path to the i4h asset for the given version.

    Args:
        version: The version of the asset to get.
        hash: The sha256 hash of the asset.

    Returns:
        The path to the i4h asset.
    """
    asset_root = _I4H_ASSET_ROOT.get(os.environ.get("I4H_ASSET_ENV", "staging"))  # FIXME: Add production asset root
    if hash is None:
        hash = get_i4h_asset_hash(version=version)
    if hash is None:
        raise ValueError(f"Invalid version: {version}")
    remote_path = f"{asset_root}/{version}/i4h-assets-v{version}-{hash}.zip"
    try:
        # Try to check if the asset exists if isaacsim simulation is started
        import omni.client
        if not omni.client.stat(remote_path)[0] == omni.client.Result.OK:
            raise ValueError(f"Asset not found: {remote_path}")
    except ImportError:
        pass

    return remote_path


def get_i4h_local_asset_path(
        version: str = "0.1.0",
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


def retrieve_asset(
    version: str = "0.1.0",
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

    try:
        import omni.client
        app = None
    except ImportError:
        from isaacsim import SimulationApp
        app = SimulationApp({"headless": True})
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
    finally:
        if app is not None:
            app.close()
