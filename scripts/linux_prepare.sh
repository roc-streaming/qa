#! /usr/bin/env bash
set -euxo pipefail

host=$QMG_ENV

ssh $host sudo apt-get update
ssh $host sudo apt-get install -y libasound2

if [[ ! -z ${ROC_PULSE_VERSION:-} ]]; then
    ssh $host sudo apt-get install -y libpulse0 libltdl7
fi

if [[ ${ROC_DEPLOY_TYPE:-none} = pulseaudio_receiver ]]; then
    ssh $host "sudo perl -ni -e 'print unless /#roc:begin/../#roc:end/' /etc/pulse/default.pa"
    cat config/roc-sink-input.pa | ssh $host sudo tee -a /etc/pulse/default.pa

    tar -C "$QMG_DIR"/config -c pulseaudio.service \
        | ssh $host sudo tar -C /etc/systemd/system -xmv

    ssh $host sudo systemctl enable pulseaudio.service
    ssh $host sudo systemctl daemon-reload
fi

if [[ ${ROC_DEPLOY_TYPE:-none} = alsa_receiver ]]; then
    tar -C "$QMG_DIR"/config -c roc-recv.service \
        | ssh $host sudo tar -C /etc/systemd/system -xmv

    ssh $host sudo systemctl enable roc-recv.service
    ssh $host sudo systemctl daemon-reload
fi
