#! /usr/bin/env bash
set -euxo pipefail

host=$QMG_ENV

ssh $host \
  brew install \
    autoconf \
    automake \
    cmake \
    gengetopt \
    libtool \
    libuv \
    make \
    ragel \
    scons \
    sox \
    speexdsp
