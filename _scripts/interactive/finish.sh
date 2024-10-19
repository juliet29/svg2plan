#!/usr/bin/env bash

run="typer app.py run"

$run  assign-remaining-subsurfaces $1
$run  save-connectivity-graph $1