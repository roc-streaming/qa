#! /usr/bin/env bash
set -euxo pipefail

host=$QMG_ENV.lan

ssh $host sudo apt-get update
ssh $host sudo apt-get install -y libasound2

if [[ ! -z ${ROC_PULSE_VERSION:-} ]]; then
    ssh $host sudo apt-get install -y libpulse0 libltdl7
fi
