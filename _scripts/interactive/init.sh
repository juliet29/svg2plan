#!/usr/bin/env bash

initialize 
run="typer app.py run"
echo $run
echo $1
$run init $1

# is same for all to begin with .. 
$run create-window $1 1 -w 2 4 0 -h 5 0 0 -hh 3 0 0 
$run create-door $1 0 -w 2 8 0 -h 6 8 0 -t 1 0 0 
$run create-door $1 1 -w 2 8 0 -h 6 8 0 -t 1 0 0



$run show-edges $1
