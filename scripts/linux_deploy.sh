#! /usr/bin/env bash
set -euxo pipefail

host=$QMG_ENV.lan
dist_dir=$(ssh $host pwd)/qmg/dist/roc-$QMG_PKG

soname=${ROC_SONAME:-${QMG_PKG%.*}}

ssh $host rm -rf $dist_dir
ssh $host mkdir -p $dist_dir
tar -C "$QMG_BIN_DIR" -cz $(ls -1 "$QMG_BIN_DIR") | ssh $host tar -C $dist_dir -xzmv

if [[ ${ROC_DEPLOY_TYPE:-none} != none ]]; then
    ssh $host sudo ln -sf \
        $dist_dir/libroc.so.$soname \
        /usr/lib/${ROC_LIB_DIR:-$ROC_TOOLCHAIN}/libroc.so.$soname

    ssh $host sudo ln -sf \
        $dist_dir/roc-send \
        /usr/bin/roc-send

    ssh $host sudo ln -sf \
        $dist_dir/roc-recv \
        /usr/bin/roc-recv

    if [[ ${ROC_DEPLOY_TYPE:-} = pulseaudio_receiver ]]; then
        ssh $host "sudo perl -ni -e 'print unless /#roc:begin/../#roc:end/' /etc/pulse/default.pa"
        cat "$QMG_DIR"/config/roc-sink-input.pa \
            | ssh $host sudo tee -a /etc/pulse/default.pa

        ssh $host mkdir -p .config/systemd/user
        tar -C "$QMG_DIR"/config -c pulseaudio.service \
            | ssh $host tar -C .config/systemd/user -xmv

        ssh $host systemctl --user enable pulseaudio.service
        ssh $host systemctl --user daemon-reload
        ssh $host whoami | xargs ssh $host sudo loginctl enable-linger

        pulse_dir=$(ssh $host "ls -d1 /usr/lib/pulse-${ROC_PULSE_VERSION}* | sort | tail -1")

        ssh $host sudo ln -sf \
            $dist_dir/module-roc-sink.so \
            $pulse_dir/modules/module-roc-sink.so

        ssh $host sudo ln -sf \
            $dist_dir/module-roc-sink-input.so \
            $pulse_dir/modules/module-roc-sink-input.so
    fi

    if [[ ${ROC_DEPLOY_TYPE:-none} = alsa_receiver ]]; then
        tar -C "$QMG_DIR"/config -c roc-recv.service \
            | ssh $host sudo tar -C /etc/systemd/system -xmv

        ssh $host sudo systemctl enable roc-recv.service
        ssh $host sudo systemctl daemon-reload
    fi

    ssh $host sudo reboot || true

    set +x

    echo "Waiting until host is down"
    while :; do
        ping -c 1 -w 1 -q $host >/dev/null 2>&1 || break
        sleep 0.2
    done

    echo "Waiting until host is up"
    while :; do
        ping -c 1 -w 1 -q $host >/dev/null 2>&1 && break
        sleep 0.2
    done
    while :; do
        ssh $host echo >/dev/null 2>&1 && break
    done

    echo "All done"
fi
