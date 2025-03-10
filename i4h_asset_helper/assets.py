import os
import shutil
import tempfile
import zipfile
from typing import Literal
import json


__all__ = [
    "get_i4h_asset_path",
    "get_i4h_local_asset_path",
    "retrieve_asset",
]

_I4H_ASSET_ROOT = {
    "nucleus": "https://isaac-dev.ov.nvidia.com/omni/web3/omniverse://isaac-dev.ov.nvidia.com",
    "staging": "",  # FIXME: Add staging asset root
    "production": "",  # FIXME: Add production asset root
}

_DEFAULT_DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), ".cache", "i4h-assets")


def _get_sha256_hash() -> dict[str, str]:
    """Get the sha256 hash for the given version."""
    with open(os.path.join(os.path.dirname(__file__), "assets_sha256.json"), "r") as f:
        return json.load(f)


def get_i4h_asset_path(version: Literal["0.1"] = "0.1") -> str:
    """
    Get the path to the i4h asset for the given version.
    """
    asset_root = _I4H_ASSET_ROOT.get(os.environ.get("ISAAC_ENV", "nucleus"))  # FIXME: Add production asset root
    hash = _get_sha256_hash().get(version, None)
    if hash is None:
        raise ValueError(f"Invalid version: {version}")
    remote_path = f"{asset_root}/Library/IsaacHealthcare/{version}/i4h-assets-v{version}-{hash}.zip"
    try:
        # Try to check if the asset exists if isaacsim simulation is started
        import omni.client
        if not omni.client.stat(remote_path)[0] == omni.client.Result.OK:
            raise ValueError(f"Asset not found: {remote_path}")
    except ImportError:
        pass

    return remote_path


def get_i4h_local_asset_path(version: Literal["0.1"] = "0.1", download_dir: str | None = None) -> str:
    """
    Get the path to the i4h asset for the given version.
    """
    if download_dir is None:
        download_dir = _DEFAULT_DOWNLOAD_DIR
    hash = _get_sha256_hash().get(version)
    return os.path.join(download_dir, hash)


def retrieve_asset(
    version: Literal["0.1"] = "0.1", download_dir: str | None = None, force_download: bool = False
) -> str:
    """
    Download the asset from the remote path to the download directory.
    """
    local_path = get_i4h_local_asset_path(version, download_dir)

    # If the asset hash is a folder in download_dir, skip the download
    if os.path.exists(local_path) and not force_download:
        return local_path

    # Force download
    if os.path.exists(local_path):
        shutil.rmtree(local_path)

    os.makedirs(local_path)

    try:
        import omni.client
    except ImportError:
        raise ImportError("isaacsim simulation is not started. It is required to download the asset.")

    remote_path = get_i4h_asset_path(version)
    result, _, file_content = omni.client.read_file(remote_path)

    if result != omni.client.Result.OK:
        raise ValueError(f"Failed to download asset: {remote_path}")

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            with open(os.path.join(temp_dir, f"i4h-assets-v{version}.zip"), "wb") as f:
                f.write(file_content)
            # TODO: Check sha256 hash
            with zipfile.ZipFile(os.path.join(temp_dir, f"i4h-assets-v{version}.zip"), "r") as zip_ref:
                zip_ref.extractall(local_path)
            return local_path
    except Exception as e:
        raise ValueError(f"Failed to extract asset: {remote_path}") from e
