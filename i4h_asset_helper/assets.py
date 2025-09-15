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
import importlib
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Tuple
from urllib.parse import urlparse

from botocore.exceptions import ClientError
from tqdm import tqdm

__all__ = [
    "get_i4h_asset_hash",
    "get_i4h_asset_path",
    "get_i4h_local_asset_path",
    "retrieve_asset",
    "BaseI4HAssets",
]

_I4H_ASSET_ROOT = {
    "dev": "https://isaac-dev.ov.nvidia.com/omni/web3/omniverse://isaac-dev.ov.nvidia.com/Library/IsaacHealthcare",
    "staging": "https://omniverse-content-staging.s3-us-west-2.amazonaws.com/Assets/Isaac/Healthcare",
    "production": "https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/Healthcare",
}


# S3 bucket mapping
_S3_BUCKETS = {
    "staging": "omniverse-content-staging",
    "production": "omniverse-content-production",
}

# S3 region mapping
_S3_REGIONS = {
    "staging": "us-west-2",
    "production": "us-west-2",
}


def _is_s3_environment() -> bool:
    """Check if current environment uses S3 for asset storage."""
    env = _get_asset_env()
    return env in ["staging", "production"]


def _parse_s3_url(url: str) -> Tuple[str, str]:
    """
    Parse S3 URL to extract bucket and key.

    Args:
        url: The S3 URL (https://bucket-name.s3-region.amazonaws.com/path/to/key)

    Returns:
        Tuple of (bucket_name, key)
    """
    parsed = urlparse(url)

    # Extract bucket name from hostname
    hostname = parsed.netloc
    if hostname.endswith(".amazonaws.com"):
        bucket = hostname.split(".s3-")[0]
    else:
        # Use mapping if hostname doesn't match expected pattern
        env = _get_asset_env()
        bucket = _S3_BUCKETS.get(env)

    # Extract key from path (remove leading slash)
    key = parsed.path
    if key.startswith("/"):
        key = key[1:]

    return bucket, key


def _get_s3_client():
    """Get boto3 S3 client with anonymous configuration for public buckets."""
    env = _get_asset_env()

    try:
        import boto3
        import botocore.config

        # Create an anonymous/unsigned config for public access
        config = botocore.config.Config(
            signature_version=botocore.UNSIGNED,
            retries={
                "max_attempts": 5,
                "mode": "adaptive",  # Use adaptive mode for exponential backoff with jitter
            },
        )

        return boto3.client("s3", region_name=_S3_REGIONS.get(env), config=config)
    except ImportError:
        raise ImportError("boto3 is required for S3 access. Install with 'pip install boto3'")


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


def _get_asset_env() -> str:
    """Get the current configuration of the asset root."""
    return os.getenv("I4H_ASSET_ENV", "production")


def _get_download_dir() -> str:
    """Get the download directory for the current configuration."""
    default_dir = os.path.join(os.path.expanduser("~"), ".cache", "i4h-assets")
    return os.getenv("I4H_ASSET_DOWNLOAD_DIR", default_dir)


def _unify_path(path: str) -> str:
    """
    Unify the path in different configurations.

    When the file is on a nucleus server, the _list_file function returns that path starting with "omniverse://".
    So we need to unify the path to the same format, if the path is not returned by the _list_file function.
    """
    if _get_asset_env() == "dev":
        return path.replace("https://isaac-dev.ov.nvidia.com/omni/web3/", "")
    return path


def _get_default_version() -> str:
    """Get the default version of the i4h asset."""
    with open(os.path.join(os.path.dirname(__file__), "assets_sha256.json"), "r") as f:
        return list(json.load(f).keys())[-1]


def get_i4h_asset_version() -> str:
    """Get the version of the i4h asset."""
    return os.getenv("I4H_ASSET_VERSION", _get_default_version())


def get_i4h_asset_hash(version: str | None = None) -> str | None:
    """Get the sha256 hash for the given version."""
    version = version if version is not None else get_i4h_asset_version()
    # Get it from the environment variable if it exists
    if os.environ.get("I4H_ASSET_SHA256_HASH"):
        return os.environ.get("I4H_ASSET_SHA256_HASH")
    # Otherwise, get it from the file
    with open(os.path.join(os.path.dirname(__file__), "assets_sha256.json"), "r") as f:
        return json.load(f).get(version, None)


def get_i4h_asset_path(version: str | None = None, hash: str | None = None) -> str:
    """
    Get the path to the i4h asset for the given version.

    Args:
        version: The version of the asset to get.
        hash: The sha256 hash of the asset.

    Returns:
        The path to the i4h asset.
    """
    asset_root = _I4H_ASSET_ROOT.get(_get_asset_env())
    version = version if version is not None else get_i4h_asset_version()

    # if the environment is not S3, the hash will be None
    if not _is_s3_environment():
        remote_path = f"{asset_root}/{version}"
        return remote_path

    hash = hash if hash is not None else get_i4h_asset_hash(version=version)
    remote_path = f"{asset_root}/{version}/{hash}"

    return remote_path


def get_i4h_local_asset_path(
    version: str | None = None, download_dir: str | None = None, hash: str | None = None
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
    version = version if version is not None else get_i4h_asset_version()
    if download_dir is None:
        download_dir = _get_download_dir()

    if not _is_s3_environment():
        return os.path.join(download_dir, version)

    hash = hash if hash is not None else get_i4h_asset_hash(version=version)

    if hash is None:
        # If no hash is available for this version, use version as directory name
        return os.path.join(download_dir, version)
    else:
        return os.path.join(download_dir, hash)


def _get_asset_relpath(url_entry: str, version: str = get_i4h_asset_version(), hash: str | None = None) -> str:
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
    asset_root = _unify_path(asset_root)

    if not url_entry.startswith(asset_root):
        raise ValueError(f"URL entry {url_entry} expects to begin with {asset_root}")

    return os.path.relpath(url_entry, asset_root)


def _is_url_folder(url_entry: str) -> bool:
    """Check if the url_entry is a folder."""

    if not _is_import_ready("omni.client"):
        if not _is_s3_environment():
            raise ValueError("Please start the isaac simulation app before the asset helper.")
        # Fallback for S3 environments: boto3
        try:
            bucket, key = _parse_s3_url(url_entry)
            s3_client = _get_s3_client()

            # For S3, a folder is indicated by a key that ends with a '/'
            # If key doesn't end with '/', check if objects exist with this prefix
            if not key.endswith("/"):
                # List objects with this prefix to see if it's a folder
                max_retries = 5
                retry_count = 0
                backoff_time = 1  # Start with 1 second

                while True:
                    try:
                        response = s3_client.list_objects_v2(Bucket=bucket, Prefix=key, Delimiter="/", MaxKeys=1)
                        # If CommonPrefixes exist, it's a folder
                        return "CommonPrefixes" in response or response.get("KeyCount", 0) > 0
                    except ClientError as e:
                        error_code = e.response.get("Error", {}).get("Code", "")
                        if error_code == "SlowDown" and retry_count < max_retries:
                            # If we hit a rate limit, wait with exponential backoff
                            retry_count += 1
                            sleep_time = backoff_time * (1 + 0.5 * (2.0**retry_count))
                            print(f"Rate limit hit. Retrying... (attempt {retry_count}/{max_retries})")
                            time.sleep(sleep_time)
                        else:
                            # If error is not rate limiting or we're out of retries, raise the exception
                            raise ValueError(f"The remote path {url_entry} returned an error: {str(e)}")
            return True
        except Exception as e:
            raise ValueError(f"The remote path {url_entry} is not valid: {str(e)}")

    import omni.client

    url_entry_unified = _unify_path(url_entry)
    result, entries = omni.client.stat(url_entry_unified)
    if result != omni.client.Result.OK:
        raise ValueError(f"The remote path {url_entry_unified} is not valid")
    return entries.size == 0


def _list_asset_url(url_entry: str) -> List[str]:
    """
    List all the items in the url_entry. When it is a folder, it will return all the items in the folder.
    When it is a file, it will return a list with the file itself.
    """
    # If not a folder, just return the url as a list with one entry
    if not _is_url_folder(url_entry):
        return [_unify_path(url_entry)]

    if not _is_import_ready("isaacsim.storage.native.nucleus"):
        if not _is_s3_environment():
            raise ValueError("Please start the isaac simulation app before the asset helper.")
        # Fallback for S3 environments: boto3
        try:
            bucket, key = _parse_s3_url(url_entry)
            s3_client = _get_s3_client()

            # Ensure key ends with '/'
            if key and not key.endswith("/"):
                key = key + "/"

            # List all objects with this prefix
            entries = []
            paginator = s3_client.get_paginator("list_objects_v2")

            # Get files with retry logic for rate limiting
            max_retries = 5
            retry_count = 0
            backoff_time = 1  # Start with 1 second

            while True:
                try:
                    # Get files
                    for page in paginator.paginate(Bucket=bucket, Prefix=key):
                        if "Contents" in page:
                            for obj in page["Contents"]:
                                # Skip the folder itself
                                if obj["Key"] != key:
                                    obj_url = f"https://{bucket}.s3-{_S3_REGIONS.get(_get_asset_env())}.amazonaws.com/{obj['Key']}"
                                    entries.append(obj_url)
                    break  # Success - exit the retry loop
                except ClientError as e:
                    error_code = e.response.get("Error", {}).get("Code", "")
                    if error_code == "SlowDown" and retry_count < max_retries:
                        # If we hit a rate limit, wait with exponential backoff
                        retry_count += 1
                        sleep_time = backoff_time * (1 + 0.5 * (2.0**retry_count))
                        print(f"Rate limit hit. Retrying... (attempt {retry_count}/{max_retries})")
                        time.sleep(sleep_time)
                    else:
                        # If error is not rate limiting or we're out of retries, raise the exception
                        raise ValueError(f"Failed to list S3 objects at {url_entry}: {str(e)}")

            return entries
        except Exception as e:
            raise ValueError(f"Failed to list S3 objects at {url_entry}: {str(e)}")

    from isaacsim.storage.native.nucleus import _list_files

    # _list_files is an async function
    _, entries = asyncio.run(_list_files(url_entry))
    return entries


def _filter_downloaded_assets(
    url_entries: List[str], local_dir: str, version: str | None = None, hash: str | None = None, verbose: bool = False
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
        local_path = os.path.join(local_dir, _get_asset_relpath(entry_url, version, hash))
        if os.path.isfile(local_path):
            if verbose:
                print(f"Asset already downloaded to: {local_path}. Skipping download.")
        else:
            results.append(entry_url)
    return results


def _download_individual_asset(url_entry: str, download_dir: str, version: str | None = None, hash: str | None = None):
    version = version if version is not None else get_i4h_asset_version()
    local_path = os.path.join(download_dir, _get_asset_relpath(url_entry, version, hash))
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    if not _is_import_ready("omni.client"):
        if not _is_s3_environment():
            raise ValueError("Please start the isaac simulation app before the asset helper.")
        # Fallback for S3 environments: boto3
        try:
            bucket, key = _parse_s3_url(url_entry)
            s3_client = _get_s3_client()

            # Download file directly to local path
            if os.path.exists(local_path):
                os.remove(local_path)

            s3_client.download_file(bucket, key, local_path)
            return local_path
        except Exception as e:
            raise ValueError(f"Failed to download asset from S3: {url_entry}: {str(e)}")

    import omni.client

    result, _, file_content = omni.client.read_file(url_entry)
    if result != omni.client.Result.OK:
        raise ValueError(f"Failed to download asset: {url_entry}")

    if os.path.exists(local_path):
        os.remove(local_path)

    with open(local_path, "wb") as f:
        f.write(file_content)

    return local_path


def _download_assets(
    url_entries: List[str],
    download_dir: str,
    version: str | None = None,
    hash: str | None = None,
    concurrency: int = 2,
    timeout: float = 3600.0,
):
    """
    Download assets from url entry sources to local directory.

    Args:
        url_entries: The url entries to download.
        download_dir: The directory to download the asset to. Default is the cache directory.
        version: The version of the asset.
        hash: The sha256 hash of the asset.
        concurrency: The number of concurrent downloads.
        timeout: The timeout for the download.

    Returns:
        The path to the local asset.
    """
    version = version if version is not None else get_i4h_asset_version()
    total = len(url_entries)

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures_to_url = {
            executor.submit(_download_individual_asset, url_entry, download_dir, version, hash): url_entry
            for url_entry in url_entries
        }

        # Use tqdm to show progress
        with tqdm(total=total, desc=f"Downloading assets to {download_dir}", unit="files") as pbar:
            for future in as_completed(futures_to_url, timeout=timeout):
                future.result()
                pbar.update(1)


def retrieve_asset(
    version: str | None = None,
    download_dir: str | None = None,
    sub_path: str | None = None,
    hash: str | None = None,
    force_download: bool = False,
    verbose: bool = False,
) -> str:
    """
    Download the asset from the remote path to the download directory.

    Args:
        version: The version of the asset to download.
        download_dir: The directory to download the asset to.
        sub_path: The sub path of the asset to download.
        hash: The sha256 hash of the asset.
        force_download: If True, the asset will be downloaded even if it already exists.
        verbose: If True, it will print more information.
    Returns:
        The path to the local asset.
    """
    version = version if version is not None else get_i4h_asset_version()
    local_dir = get_i4h_local_asset_path(version, download_dir, hash)
    remote_path = get_i4h_asset_path(version, hash)

    if sub_path is not None:
        remote_path = remote_path + "/" + sub_path

    paths = _list_asset_url(remote_path)

    if force_download:
        url_entries = paths
    else:
        url_entries = _filter_downloaded_assets(paths, local_dir, version, hash, verbose)

    if len(url_entries) > 0:
        _download_assets(url_entries, local_dir, version, hash)

    return local_dir


class BaseI4HAssets:
    """
    Base class for i4h assets with public attributes defining the relative paths to the assets.

    When accessing any public attribute of this class, the corresponding asset will be automatically downloaded
    if it doesn't exist locally. For USD files (with extensions .usd, .usda, or .usdc), the entire directory
    containing the file will be downloaded to ensure all dependencies are available. If skip_download_usd is True,
    USD files will use the remote path directly without downloading.

    The downloaded assets will be stored in the specified download directory (defaults to ~/.cache/i4h-assets).
    """

    def __init__(
        self, download_dir: str | None = None, skip_download_usd: bool = False, recursive_file_check: bool | None = None
    ):
        """
        Initialize the assets

        Args:
            download_dir: The directory to download the assets to
            skip_download_usd: If True, it will always use the USD file from the remote asset path. Default is False.
            recursive_file_check: If True, it will check recursively into the folder and see if every file is ready.
                When the environment is not S3, it will be set to False automatically, otherwise it will be set to True.
        """
        self._remote_asset_path = get_i4h_asset_path()
        self._download_dir = _get_download_dir() if download_dir is None else download_dir
        self._skip_download_usd = skip_download_usd
        if recursive_file_check is None:
            self._recursive_file_check = _is_s3_environment()
        else:
            self._recursive_file_check = recursive_file_check

    def __getattribute__(self, name):
        """Override to print a message when any attribute is accessed."""
        if name.startswith("_"):
            # skip the private attributes
            return super().__getattribute__(name)

        value = super().__getattribute__(name)
        if Path(value).suffix in [".usd", ".usda", ".usdc"]:
            if self._skip_download_usd:
                # return the remote asset path and skip the download
                return os.path.join(self._remote_asset_path, value)
            else:
                # A single USD file can depend on other files in the same directory.
                # Need to download the directory instead.
                _value = os.path.dirname(value)
        else:
            _value = value

        if not self._recursive_file_check:
            local_path = get_i4h_local_asset_path(download_dir=self._download_dir)
            local_sub_path = os.path.join(local_path, value)
            if os.path.isdir(local_sub_path) or os.path.isfile(local_sub_path):
                return local_sub_path

        # trigger download of the asset
        local_path = retrieve_asset(download_dir=self._download_dir, sub_path=_value)
        return os.path.join(local_path, value)
