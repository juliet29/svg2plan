#!/usr/bin/env bash
set -e # STOP if anything fail
run="uv run svg2plan-cli"

$run  assign-remaining-subsurfaces $1

$run show-edges $1

$run  save-connectivity-graph $1