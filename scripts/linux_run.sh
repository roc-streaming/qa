#! /usr/bin/env bash
set -euxo pipefail

host=$QMG_ENV.lan
dist_dir=$(ssh $host pwd)/qmg/dist/roc-$QMG_PKG

tests="$(ssh $host ls -1 $dist_dir | grep roc-test)"

for t in $tests; do
    ssh $host $dist_dir/$t
done
