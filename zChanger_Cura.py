# DEfine the patterns of layer's height
layer_height_pattern = {
    0: 0.100,
    1: 0.110,
    2: 0.130,
    3: 0.150,
    4: 0.170,
    5: 0.200,
    6: 0.210,
    7: 0.230,
    8: 0.250,
    9: 0.270,
    10: 0.290,
    11: 0.300,
    12: 0.320
    #4: 0.400
}

layer_flow_pattern = {
    0: 50,
    1: 90,
    2: 90,
    3: 100
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


# def extract_z_origin_value(input_file):
#     """
#     This function aims to find the first value of Z in order to start with the accurate value
#     """
#     with open(input_file, 'r') as file:
#         process_began = False
#         for line in file:
#             if line.startswith(';LAYER:0'):
#                 process_began = True
            
#             if process_began:
#                 if ' Z' in line:  # ' Z' to ensure we're finding Z as a standalone command
#                     parts = line.split()
#                     for part in parts:
#                         if part.startswith('Z'):
#                             z_value = float(part[1:])  # Extract the numeric part of Z
#                             #print(z_value)
#                             return z_value
#     return None  # If no Z value is found





def write_new_code(output_file, lines,flowrate_change_on=False):
    current_layer = 0 
    current_Z = 0 # extract_z_origin_value(input_file)
    Z_found = False
    new_layer = False
    with open(output_file, 'w') as out_file:
        for line in lines:

            
            if  flowrate_change_on:
                if max_nb_pattern != len(layer_flow_pattern):
                    print("Error : Height and flow patterns are not in the same number")

                if line.startswith(';LAYER:'): # The following line's where we have to change z's value.
                    new_layer = True

            #this block find the Z value and changes it

            if Z_found:
                new_z_value = current_Z + layer_height_pattern[(current_layer) % max_nb_pattern]
                current_Z = new_z_value
                modified_line = modify_gcode_line(line, new_z_value)
                out_file.write(modified_line + '\n')
                Z_found = False
            else:
                out_file.write(line)

            if new_layer: #we write the flow rate change command at the begining of the layer
                out_file.write( f"{'M221 S'}{layer_flow_pattern[(current_layer) % max_nb_pattern]}" + '\n')
                new_layer = False

            if line.startswith(';MESH:NONMESH'): # The following line's where we have to change z's value.
                Z_found = True
                current_layer += 1

            
    print("Z changed successfully")
                    


if __name__ == "__main__":    
    #We open the gcode
    with open(input_file, 'r') as file:
        code = file.readlines()

    write_new_code(output_file,code)
   
    