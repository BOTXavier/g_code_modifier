# Gcodes Modifyer

## Introduction

This project aims to allow the user to create repetitive patterns of microstructure with 3D Printers, by modifying each layer's height.

Why doing this ? 
As researchers, it allows us to study the wetting properties of such structures.

## How does it work

First of all, **your 3D file must have been sliced in 0.05mm layer's height**. Otherwise it won't work, and I still can't find why.
Probably because the slicer slices the piece with parameters depending on the layer's height, and sets a too big flow rate for smaller layer height.

Then you bring your gcode in the same file than the script.

After this step, you open the script, you'll see `input_file = ' test.gcode ' `. Just insert the name of your gcode between the quotes.

Under, you'll see   `layer_height_pattern ` and `layer_flow_pattern `. Here you have to insert the pattern you want, following the example. 
- For the layer height, **the unit is the mm**
- For the flow rate, **use %age**

Before running the system, make sure the number of layer are the same in both layer height and flow rate pattern. Otherwise, the script will alert you by printing the error.

