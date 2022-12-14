#! /usr/bin/env bash
set -euxo pipefail

host=$QMG_ENV.lan
work_dir=$(ssh $host pwd)/qmg/work/roc

src_dir=$work_dir/$(realpath --relative-to="$QMG_DIR" "$QMG_SRC_DIR")

ssh $host rm -rf $src_dir
ssh $host mkdir -p $src_dir

ssh $host git clone --recurse-submodules -b ${ROC_COMMIT:-v$QMG_PKG} \
    https://github.com/roc-streaming/roc-toolkit.git $src_dir
