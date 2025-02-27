# svg2plan

*Transform SVGs into floorplans that are valid for creation of energy models. *

![Going from marked up floor plan as svg, to EnergyPlus compliant plan](<figures/red_b1_figs/Closed Gaps.png>)
![Rectangular shape is ideal for use with the Airflow Network](<figures/red_b1_figs/Closed Gaps.png>)



This interactive, command-line based module allows you to mark up a rasterized floor plan (pdf or image) quickly and get out a floorplan that is rectangular, and has no holes or overlaps. This makes them valid not just for use in EnergyPlus, but also with EnergyPlus's Airflow Network. You can also export connectivy information, which makes it simple to add doors and windows. This makes understanding how ventilation flows through floor plans a "breeze". 

This module is meant to be paired with `plan2eplus` which generates Airflow Network-enabled EnergyPlus models.


## Running cases 

1. **Install.** Git clone this module. UV is used as the package manager. Run the `/tests` to help ensure your environment is set up correctly. 
2. **Prepare.** Mark up your floor plan with rectangles and room names and export a .svg file (software like Figma is ideal) to `svg_imports`. The .svg file should have rectangular objects with height, width, x, y, and an id. See `/svg_imports` for examples. Take note of a pixel length dimension relative to a room length (feet and inches is used here).  This information will be used to rescale the plan. 
3. **Initialize.** Run the initialization script on your command line. You will have to make it an executable. On Mac, the command is `chmod +x <script>`. The script is `/src/svg2plan/cli/scripts/init.sh`. Add the name of your svg file afterwards. So on the command line you would enter `/src/svg2plan/cli/scripts/init.sh <your-svg-file.svg>`. You can optionally add dimensional information to rescale the plan. Otherwise defaults will be used. Add `--help` for more information. This script will:
   * Create a directory for the case outputs in `/outputs3/case_<your-svg-file>`
   * Analyze the .svg file and 
      * Extract information about the room dimensions
      * Extract information about the relative adjacencies of the rooms
      * Try to resolve existing problems with the plan (eliminate holes and overlaps)
        * This is an iterative process (that should complete in seconds), and less than 10 iterations are typically needed. If the process fails because it exceeds the max iterations, try splitting up the plan or using rectangles have more similar sizes. 
    * Initialize some default door and window information 
    * Invite you to note which adjacent edges should be part of the *connectivity graph*. I.e., which edge connections denote doors and windows. Having the actual floor plan open in order to see where the windows and doors are helps here!
4. **Assign.** Once you have noted where doors and windows are, you can optionally run 
   * `uv run svg2plan-cli assign-connectivity <your-svg-file.svg>` if you want to iterate on the connections you have assigned.
   * `uv run svg2plan-cli assign-subsurfaces <your-svg-file.svg>` to denote where certain types of doors and windows should be.
   * `uv run svg2plan-cli create-window <your-svg-file.svg>` or `uv run svg2plan-cli create-door <your-svg-file.svg>`to add different types of doors and windows. 
   * Note these commands are called differently from the initializatiion script in Part 3. That script (and the `finish.sh` script that will be discussed shortly), are made up of a series of commands. To see all possible commands, type `uv run svg2plan-cli --help` for help. Add the `--h` flag after any commands to see the required arguments. 
5. **Complete.** Once all assignments have been made, `/src/svg2plan/cli/scripts/finish.sh <your-svg-file.svg>` will give assignments to all unassigned edges and save the connectivity graph. You can see the results in `/outputs3/case_<your-svg-file>`.
   * `plan.json` will hold dimensions and location of the corrected floor plan in 
   * `graph.json` will hold the assigned connectivity information 
   * `gubsurfaces.json` has information about the doors and windows
   * `config.txt` has information about the dimensional scaling used to produce the plan 
   * the `.pkl` files contain intermediate information used in processing. 
  

  