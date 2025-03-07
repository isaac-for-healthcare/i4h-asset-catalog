## I4H Assets Catalog Helper

Isaac4Health assets are stored in a zip file in the remote server path. We provide a helper to download the assets and extract them to the local directory.

### Installation

```bash
git clone git@github.com:isaac-for-healthcare/i4h-asset-catalog.git  # FIXME: change to HTTPS/Make a release
cd i4h-asset-catalog
pip install -e .
```

### Usage

We also provide a function to download the asset to a local directory (default is `~/.cache/i4h-assets/<sha256_hash>`).

```python
from isaacsim import SimulationApp
simulation_app = SimulationApp({"headless": True})

from utils.assets import retrieve_asset
local_asset_path = retrieve_asset()
print(f"Asset downloaded to: {local_asset_path}")
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