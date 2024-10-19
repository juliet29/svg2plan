#!/usr/bin/env bash
set -e # STIP if anything fails
# initialize 
run="typer app.py run"
echo $run
echo $1
$run init $1

# is same for all to begin with .. 
# all subsurfaces are the same to begin.. 


$run clean-up-domains $1

$run copy-existing-subsurfaces $1

$run show-edges $1

# can open assign.sh before had a ., need to remove what is after the .