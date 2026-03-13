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

from .assets import _get_default_version, _get_download_dir, _is_s3_environment, retrieve_asset, verify_asset


def retrieve_main():
    """Command line interface for i4h asset helper."""

    parser = argparse.ArgumentParser(
        description="Isaac for Healthcare Asset Helper", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--version", type=str, default=_get_default_version(), help="Asset version to retrieve")
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
    parser.add_argument("--skip-download", action="store_true", help="Skip downloading and only verify existing assets")
    parser.add_argument(
        "--verify", action="store_true", help="Verify the SHA-256 hash of downloaded assets after download"
    )
    args = parser.parse_args()

    use_omni = args.force_omni_client or not _is_s3_environment()
    if use_omni:
        from isaacsim import SimulationApp

        app = SimulationApp({"headless": True})

    if not args.skip_download:
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
    else:
        print(f"Skipping download for version: {args.version}")

    if args.verify:
        passed = verify_asset(
            version=args.version,
            download_dir=args.download_dir,
            hash=args.hash,
        )
        if not passed:
            if use_omni:
                app.close()
            return 1

    if use_omni:
        app.close()
    return 0


if __name__ == "__main__":
    sys.exit(retrieve_main())
