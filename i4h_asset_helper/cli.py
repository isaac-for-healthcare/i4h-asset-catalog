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

import argparse
import sys

from isaacsim import SimulationApp

from .assets import _get_download_dir, _is_s3_environment, retrieve_asset


def retrieve_main():
    """Command line interface for i4h asset helper."""

    parser = argparse.ArgumentParser(
        description="Isaac for Healthcare Asset Helper", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--version", type=str, default="0.2.0", choices=["0.2.0"], help="Asset version to retrieve")
    parser.add_argument("--force", action="store_true", help="Force download even if assets already exist")
    parser.add_argument("--download-dir", type=str, default=_get_download_dir(), help="Directory to download assets to")
    parser.add_argument(
        "--sub-path",
        type=str,
        default=None,
        help=(
            "Either a subfolder path or a subfile path under the asset catalog. "
            "Only support a single path, like `Robots`"
        ),
    )
    parser.add_argument("--hash", type=str, default=None, help="Hash of the asset to retrieve")
    parser.add_argument("--force_omni_client", action="store_true", help="Force use of omni.client.")
    args = parser.parse_args()
    # To enable the omniverse plugins
    if args.force_omni_client or not _is_s3_environment():
        app = SimulationApp({"headless": True})
    print(f"Retrieving assets for version: {args.version}")
    local_path = retrieve_asset(
        version=args.version,
        download_dir=args.download_dir,
        sub_path=args.sub_path,
        hash=args.hash,
        force_download=args.force,
        verbose=True,
    )
    print(f"Assets downloaded to: {local_path}")
    if args.force_omni_client or not _is_s3_environment():
        app.close()
    return 0


if __name__ == "__main__":
    sys.exit(retrieve_main())
