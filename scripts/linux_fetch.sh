#! /usr/bin/env bash
set -euxo pipefail

git clone --recurse-submodules -b ${ROC_COMMIT:-v$QMG_PKG} \
    https://github.com/roc-streaming/roc-toolkit.git roc-toolkit

git clone \
    https://github.com/roc-streaming/roc-pulse.git \
    roc-pulse
