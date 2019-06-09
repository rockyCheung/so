#!/usr/bin/env bash
pgrep -f sohot >> pid
pkill -f sohot
rm -f pid