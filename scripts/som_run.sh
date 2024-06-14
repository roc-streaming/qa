#! /usr/bin/env bash
set -euxo pipefail

host=$QMG_ENV.lan
dist=/root/qmg

if ssh $host mount | grep -q $dist; then
    ssh $host umount $dist
    ssh $host rmdir $dist
fi

ssh $host mkdir -p $dist
ssh $host mount -t tmpfs -o size=20m tmpfs $dist

cd "$QMG_BIN_DIR"

ls -1 | grep 'roc-test-' | grep -v 'roc-test-sndio' | while read t; do
    tar -cz $t | ssh $host tar -C $dist -xzv
    ssh $host $dist/$t </dev/null
    ssh $host rm $dist/$t </dev/null
done
