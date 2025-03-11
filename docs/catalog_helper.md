## I4H Assets Catalog Helper

### Installation

```bash
git clone git@github.com:isaac-for-healthcare/i4h-asset-catalog.git  # FIXME: change to HTTPS/Make a release
cd i4h-asset-catalog
pip install -e .
```

### Usage

To download the asset to a local directory (default is `~/.cache/i4h-assets/<_SHA256_HASH>`).

#### CLI Usage

- You must have a display (either physical or virtual) and a web browser (e.g. Chrome) to authenticate in the first run if you are using the Nucleus for development.

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

Alternatively, you can also use the `omni.client.read_file` or `omni.isaac.lab.utils.assets.retrieve_file_path` API to read or download the asset in `asset_path` manually.

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
