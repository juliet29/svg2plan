#!/usr/bin/env bash
set -e # STOP if anything fails

# initialize 
run="uv run svg2plan-cli"
echo $run
echo $1
$run init $1 --reset

# is same for all to begin with .. 
# all subsurfaces are the same to begin.. 


$run clean-up-domains $1

$run copy-existing-subsurfaces $1

$run show-edges $1

$run assign-connectivity $1

echo "Next steps: Run svg2plan-cli assign-connectivity (again) or svg2plan-cli assign-subsurfaces. To create more windows or doors run create-window or create-door. Current case name is $1"

# can open assign.sh before had a ., need to remove what is after the .