#! /usr/bin/env bash
set -euxo pipefail

docker_image=${ROC_TOOLCHAIN_IMAGE:-rocstreaming/toolchain-$ROC_TOOLCHAIN}

docker_pull() {
    docker pull ${docker_image}
}

docker_run() {
    docker run -t --rm -u $UID -v "$QMG_SRC_DIR:$QMG_SRC_DIR" -w "$QMG_SRC_DIR" \
      ${docker_image} "$@"
}

scons_3rdparty="all"
if [ ! -z "${ROC_PULSE_VERSION:-}" ]; then
    scons_3rdparty="${scons_3rdparty},pulseaudio:$ROC_PULSE_VERSION"
fi

scons_opts=(
    --enable-tests
)
if [[ -z ${ROC_PULSE_VERSION:-} ]]; then
    scons_opts+=(
        --disable-pulseaudio
    )
fi

scons_host=${ROC_TOOLCHAIN_PREFIX:-}
if [[ -z ${ROC_TOOLCHAIN_PREFIX+x} ]]; then
    scons_host=${ROC_TOOLCHAIN}
fi

scons_cmd=(
  scons -Q -C roc-toolkit \
    ${scons_opts[@]} \
    --prefix="$QMG_SRC_DIR/roc-dist" \
    --host=${scons_host} \
    --build-3rdparty=$scons_3rdparty
)

docker_pull
docker_run ${scons_cmd[@]}
docker_run ${scons_cmd[@]} install

cp -a "$QMG_SRC_DIR"/roc-toolkit/bin/$ROC_TOOLCHAIN/* "$QMG_BIN_DIR"/

if [[ ${ROC_DEPLOY_TYPE:-none} = pulseaudio_receiver ]]; then
    rm -rf roc-pulse/build/$ROC_TOOLCHAIN

    docker_run \
      cmake -S roc-pulse -B roc-pulse/build/$ROC_TOOLCHAIN \
        -DDOWNLOAD_ROC=OFF \
        -DROC_INCLUDE_DIR="$QMG_SRC_DIR/roc-dist/include" \
        -DROC_LIB_DIR="$QMG_SRC_DIR/roc-dist/lib" \
        -DTOOLCHAIN_PREFIX=$ROC_TOOLCHAIN \
        -DPULSEAUDIO_VERSION=$ROC_PULSE_VERSION

    docker_run \
      make --no-print-directory -C roc-pulse/build/$ROC_TOOLCHAIN

    cp -a "$QMG_SRC_DIR"/roc-pulse/bin/* "$QMG_BIN_DIR"/
fi
