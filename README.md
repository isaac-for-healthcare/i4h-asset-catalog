# i4h-asset-catalog


The Isaac for Healthcare (i4h) asset catalog is a collection of assets that are used to create the i4h simulation environment.

The asset catalog follows the Isaac Lab asset structure. You can find the asset for each version in the corresponding folders.

- [Version 0.1](./docs/catalog_v0.1.md)

You can also use the `i4h_asset_helper` package to get the download links for the assets.
For more details, please refer to [I4H Assets Catalog Helper](./docs/catalog_helper.md).

```python
from i4h_asset_helper import get_i4h_asset_path
print(get_i4h_asset_path())
```
