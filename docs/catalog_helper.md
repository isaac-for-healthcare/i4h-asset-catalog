## I4H Assets Catalog Helper

### Requirements

- Python 3.10

### Installation

It is recommended to use a virtual environment like `conda` as described in the [IsaacSim Pip Installation Guide](https://docs.isaacsim.omniverse.nvidia.com/4.5.0/installation/install_python.html#installation-using-pip).

```bash
conda create -n i4h-assets python=3.10
conda activate i4h-assets
git clone https://github.com/isaac-for-healthcare/i4h-asset-catalog.git
cd i4h-asset-catalog
pip install -e .
```

### Usage

To download the asset to a local directory `~/.cache/i4h-assets/<SHA256_HASH>`:

### Python Usage

```python
from i4h_asset_helper import BaseI4HAssets

class MyAssets(BaseI4HAssets):
    """Assets manager for the your workflow."""
    dVRK_ECM = "Robots/dVRK/ECM/ecm.usd"


my_assets = MyAssets()

# When you use the asset, it will check if the asset is downloaded.
# If not, it will download the asset to the default download directory.
print(my_assets.dVRK_ECM)
```

#### CLI Usage

```bash
i4h-asset-retrieve [-h] [--version ] [--force] [--download-dir DOWNLOAD_DIR] [--sub-path SUB_PATH] [--hash HASH] [--force_omni_client]
```

##### Options:
- `-h, --help`: Show help message and exit
- `--version`: Asset version to retrieve (default: the latest version)
- `--force`: Force download even if assets already exist (default: False)
- `--download-dir DOWNLOAD_DIR`: Directory to download assets to (default: ~/.cache/i4h-assets)
- `--sub-path SUB_PATH`: Either a subfolder path or a subfile path under the asset catalog. Only support a single path, like `Robots` or `Robots/Franka` (default: None)
- `--hash HASH`: Hash of the asset to retrieve (default: None)
- `--force_omni_client`: Force use of omni.client. (default: False)

##### Example:
```bash
# Download a specific subfolder of assets
i4h-asset-retrieve --sub-path Robots

# Download assets with a specific hash
i4h-asset-retrieve --hash abc123def456

# Force re-download of assets to a custom directory
i4h-asset-retrieve --force --download-dir ~/my-assets
```

### Environment Variables


#### I4H_ASSET_DOWNLOAD_DIR

- You can set the `I4H_ASSET_DOWNLOAD_DIR` environment variable to the directory to download assets to.
- The default directory is `~/.cache/i4h-assets`.
- A subfolder with the hash of the asset will be created in this directory.

#### I4H_ASSET_ENV

- There are three different asset server environments: `dev`, `staging`, and `production`. `staging` and `production` are publicly accessible and `dev` is only accessible by the internal team. You can set the `I4H_ASSET_ENV` environment variable to `dev`, `staging`, or `production` to use the corresponding asset server.
- The current default environment is `production`.
- If you use the `dev` environment, i.e. `export I4H_ASSET_ENV=dev`, you must have a display (either physical or virtual) and a web browser (e.g. Chrome) to authenticate in the first run.

#### I4H_ASSET_SHA256_HASH

- SHA256 hash of the asset zip package is used to version the asset in the development process.
- You can set the `I4H_ASSET_SHA256_HASH` environment variable to the sha256 hash of the asset to retrieve.
- When you use the CLI, you can use the `--hash` argument to specify the hash.
  - Priority order: CLI argument > environment variable > `assets_sha256.json` file in the `i4h_asset_helper` package.
