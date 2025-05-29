#!/usr/bin/env sh

case $1 in
clean)
    make clean
    make -f images.mk clean
    ;;
*)
    make -f images.mk
    make html
    ;;
esac
