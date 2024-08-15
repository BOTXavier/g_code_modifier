# Gcodes Modifyer

## Introduction

This project aims to allow the user to create repetitive patterns of microstructure with 3D Printers, by modifying each layer's height.

Why doing this ? 
As researchers, it allows us to study the wetting properties of such structures.

## How does it work

First of all, **your 3D file must have been sliced in 0.05mm layer's height**. Otherwise it won't work, and I still can't find why.
Probably because the slicer slices the piece with parameters depending on the layer's height, and sets a too big flow rate for smaller layer height.

**Step 1:** 
You bring your gcode in the same file than the script.

**Step 2:** 
You open the script, you'll see `input_file = ' test.gcode ' `. Just insert the name of your gcode between the quotes.

Under, you'll see   `layer_height_pattern ` and `layer_flow_pattern `. Here you have to insert the pattern you want, following the example. 
- For the layer height, **the unit is the mm**. Be sure to stay between 0.32 and 0.05mm
- For the flow rate, **use %age**. Be sure to stay between 80 and 200%

Before running the system, make sure the number of layer are the same in both layer height and flow rate pattern. Otherwise, the script will alert you by printing the error.

**Step 3:** 
You scroll down until you find the `if __name__ == "__main__": `
There, you'll find the `write_new_code(output_file, code,True)`line. Here you'll have to modify the 3rd parameter. If it is set to `True`, the script will take into account the flowrate parameters. If sent on `False`, the programm will only change the layer's height without changing the flow rate.

**Step 4:** 
Run the script ! If it worked, it will print a success message in the console, and you'll find the modified file in the same folder, with the name " modified_* *original_name* *".

**Step 5:** 
Copy the new file in your USB stick, click it in the printer, and here we go ! 

### Features not included 

The Slicer slice the object for given dimensions. This program doesn't take into account the dimensions correspondance. Indeed, as we change the layer height, we would need to change the number of layer to fit the dimensions of the original object. 
For example : if we slice a 1mm object with 0.1mm layer's height, there will be 10 layers. After my program, if we change the dimensions to a pattern with 0.1 and 0.2mm height, the dimension expected is therefor 1.5mm

The script is compatible only with the prusa slicer. There is also a script compatible with Cura, but I didn't check yet if it still works or not. It may not work with any other slicers as the produce a gcode written differently. Those scripts has been made by carefully studying the codes generatade by Cura's slicer and Prusa's slicer, for the printer possessed in the University of Otago.

##Contributors
These scripts have been made by Xavier Dartevel


