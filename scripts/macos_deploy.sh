#! /usr/bin/env bash
set -euxo pipefail

host=$QMG_ENV.lan
work_dir=$(ssh $host pwd)/qmg/work/roc
dist_dir=$(ssh $host pwd)/qmg/dist/roc-$QMG_PKG

bin_dir=$work_dir/$(realpath --relative-to="$QMG_DIR" "$QMG_BIN_DIR")

ssh $host rm -rf $dist_dir
ssh $host mkdir -p $(dirname $dist_dir)
ssh $host cp -a $bin_dir $dist_dir
