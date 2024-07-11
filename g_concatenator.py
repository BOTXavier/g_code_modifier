


## We want to use N files as input files, and concatenate them into one file, in order to change the layer's height of one object.
# Input : N gcodes
# Output : 1 gcode 
# For each layer, we want to replace the data inside the layer by the data in the file n, with n belonging to [1,N]
# exemple :  3input files. layer1, we get the data of file 1 until layer2.
# layer 2, we get the data from the file2
# layer 3 : we get the data from file 3
# layer4 : we get the data from file 1. etc.

#This script isn't usable. It stays here just as "historical"

def mix_gcodes(input_files, output_file):
    # Read all G-code files and store their layer data
    layer_data = []
    for file in input_files:
        with open(file, 'r') as f:
            lines = f.readlines()
        
        # Extract layer data
        layers = []
        current_layer = []
        for line in lines:
            if line.startswith(';LAYER:'):
                if current_layer:
                    layers.append(current_layer)
                current_layer = [line]
            else:
                current_layer.append(line)
        
        if current_layer:
            layers.append(current_layer)
        
        layer_data.append(layers)

    # Determine the maximum number of layers across all files
    max_layers = max(len(layers) for layers in layer_data)
    
    # Open the output file to write the mixed G-code
    with open(output_file, 'w') as out_file:
        for layer_index in range(max_layers):
            # Determine which file to use for the current layer
            file_index = layer_index % len(input_files)
            # Check if the current file has the current layer
            if layer_index < len(layer_data[file_index]):
                # Write the current layer from the current file to the output file
                out_file.writelines(layer_data[file_index][layer_index])


# List of input G-code files
input_files = ['test03.gcode', 'test025.gcode', 'test02.gcode']

# Output G-code file
output_file = 'combined_file.gcode'

# Call the function to concatenate G-code files
mix_gcodes(input_files, output_file)
