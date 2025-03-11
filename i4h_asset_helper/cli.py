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

from .assets import retrieve_asset


def retrieve_main():
    """Command line interface for i4h asset helper."""

    parser = argparse.ArgumentParser(description="Isaac for Healthcare Asset Helper")
    parser.add_argument(
        "--version",
        type=str,
        default="0.1",
        choices=["0.1"],
        help="Asset version to retrieve"
    )
    parser.add_argument(
        "--download-dir",
        type=str,
        default=None,
        help="Directory to download assets to"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force download even if assets already exist"
    )

    args = parser.parse_args()
    print(f"Retrieving assets for version: {args.version}")
    local_path = retrieve_asset(
        version=args.version,
        download_dir=args.download_dir,
        force_download=args.force
    )
    print(f"Assets downloaded to: {local_path}")
    return 0


if __name__ == "__main__":
    sys.exit(retrieve_main())
