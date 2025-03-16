## I4H Assets Catalog Helper

### Installation

```bash
git clone git@github.com:isaac-for-healthcare/i4h-asset-catalog.git  # FIXME: change to HTTPS/Make a release
cd i4h-asset-catalog
pip install -e .
```

### Usage

To download the asset to a local directory (default is `~/.cache/i4h-assets/<_SHA256_HASH>`):

#### CLI Usage


```bash
i4h-asset-retrieve
```

- **NOTE**: This is a blocking function and may cause hitches or hangs in the UI. The following warning is expected:

```
[108,322ms] [Warning] [omni.client.python] Detected a blocking function. This will cause hitches or hangs in the UI. Please switch to the async version:
  File "<path>/bin/i4h-asset-retrieve", line 8, in <module>
  File "<path>/i4h_asset_helper/cli.py", line 47, in retrieve_main
  File "<path>/i4h_asset_helper/assets.py", line 120, in retrieve_asset
  File "<path>/omni/extscore/omni.client/omni/client/__init__.py", line 610, in read_fil
```

#### Python Usage

```python
from isaacsim import SimulationApp
from i4h_asset_helper import get_i4h_asset_path, retrieve_asset

simulation_app = SimulationApp({"headless": True})

local_asset_path = retrieve_asset()
print(f"Asset downloaded to: {local_asset_path} from {get_i4h_asset_path()}")

simulation_app.close()
```

You can pass the `download_dir` argument to the `retrieve_asset` function to download the asset to a specific directory.

```python
local_asset_path = retrieve_asset(download_dir="~/Downloads")
```

It needs to be noted that the user needs to configure the asset path in applications accordingly if they want to use the local asset path other than the default one.


If you want to use the native API to read or download the asset, you can use the `omni.client.read_file` or `omni.isaac.lab.utils.assets.retrieve_file_path` API.

```python
from isaacsim import SimulationApp
simulation_app = SimulationApp({"headless": True})

import omni.client
from utils.assets import get_i4h_asset_path

asset_path = get_i4h_asset_path()

result, _, file_content = omni.client.read_file(asset_path)
with open("i4h-assets-v0.1.zip", "wb") as f:
    f.write(file_content)

simulation_app.close()
```

### Environment Variables

#### I4H_ASSET_ENV

- There are three different asset server environments: `dev`, `staging`, and `production`. `staging` and `production` are publicly accessible and `dev` is only accessible by the internal team. You can set the `I4H_ASSET_ENV` environment variable to `dev`, `staging`, or `production` to use the corresponding asset server.
- The current default environment is `staging`. (FIXME: update this once we have a production release)
- If you use the `dev` environment, i.e. `export I4H_ASSET_ENV=dev`, you must have a display (either physical or virtual) and a web browser (e.g. Chrome) to authenticate in the first run.

#### ISAAC_ASSET_SHA256_HASH

- SHA256 hash of the asset zip package is used to version the asset in the development process.
- You can set the `ISAAC_ASSET_SHA256_HASH` environment variable to the sha256 hash of the asset to retrieve.
- When you use the CLI, you can use the `--hash` argument to specify the hash.
  - Priority order: CLI argument > environment variable > `assets_sha256.json` file in the `i4h_asset_helper` package.
