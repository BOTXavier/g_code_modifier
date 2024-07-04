# Définir le motif des layer's height
layer_height_pattern = {
    0: 0.100,
    1: 0.200,
    2: 0.300,
    3: 0.400
    #4: 0.400
}


input_file = 'test.gcode'              # Name of the gfile you want to modify
output_file = 'Modified_' + input_file     # name of the gfile you want to get after the process.

max_nb_pattern = len(layer_height_pattern)



def modify_gcode_line(line, new_value):
    """
    Modify the value of Z axis in a G-code line.

    :param line: The original G-code line.
    :param new_value: The new value for the specified axis.
    :return: The modified G-code line.
    """
    parts = line.split()
    for i, part in enumerate(parts):
        if part.startswith("Z"):
            parts[i] = f"{'Z'}{new_value}"
            break
    return ' '.join(parts)


def extract_z_origin_value(input_file):
    """
    This function aims to find the first value of Z in order to start with the accurate value
    """
    with open(input_file, 'r') as file:
        process_began = False
        for line in file:
            if line.startswith(';LAYER:0'):
                process_began = True
            
            if process_began:
                if ' Z' in line:  # ' Z' to ensure we're finding Z as a standalone command
                    parts = line.split()
                    for part in parts:
                        if part.startswith('Z'):
                            z_value = float(part[1:])  # Extract the numeric part of Z
                            #print(z_value)
                            return z_value
    return None  # If no Z value is found


#We open the gcode
with open(input_file, 'r') as file:
    lines = file.readlines()

current_layer = 0 
current_Z = 0 # extract_z_origin_value(input_file)
Z_found = False

with open(output_file, 'w') as out_file:
    for line in lines:

        if Z_found:
            new_z_value = current_Z + layer_height_pattern[(current_layer) % max_nb_pattern]
            current_Z = new_z_value
            modified_line = modify_gcode_line(line, new_z_value)
            out_file.write(modified_line + '\n')
            Z_found = False
        else:
            out_file.write(line)

        if line.startswith(';MESH:NONMESH'): # The following line's where we have to change z's value.
            Z_found = True
            current_layer += 1

        #we write the new script 
        

    

    






#Each time we find a line with Z: we change by Z + layer_pattern