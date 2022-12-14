#! /usr/bin/env bash
set -euxo pipefail

host=$QMG_ENV.lan
work_dir=$(ssh $host pwd)/qmg/work/roc

src_dir=$work_dir/$(realpath --relative-to="$QMG_DIR" "$QMG_SRC_DIR")
bin_dir=$work_dir/$(realpath --relative-to="$QMG_DIR" "$QMG_BIN_DIR")

ssh $host \
  scons -Q -C $src_dir \
    --enable-tests \
    --build-3rdparty=openfec

ssh $host rm -rf $bin_dir
ssh $host mkdir -p $(dirname $bin_dir)
ssh $host cp -a $src_dir/bin/$ROC_TOOLCHAIN $bin_dir
