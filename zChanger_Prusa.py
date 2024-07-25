# DEfine the patterns of layer's height
layer_height_pattern = {
    0: 0.100,
    1: 0.200,
    2: 0.300,
    3: 0.350
    #4: 0.400
}

layer_flow_pattern = {
    0: 50,
    1: 90,
    2: 90,
    3: 100
    #4: 0.400
}


input_file = 'test_prusa_wout_wipe.gcode'              # Name of the gfile you want to modify
output_file = 'Modified_' + input_file     # name of the gfile you want to get after the process.

max_nb_pattern = len(layer_height_pattern)
if max_nb_pattern != len(layer_flow_pattern):
    print("Error : Height and flow patterns are not in the same number")


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
    New_Z_Value = 0
    previous_current_Z = 0
    previous_Z = 0
    previous_layer_originZ = 0
    New_layer = False

    
    with open(output_file, 'w') as out_file:
        for line in lines:

            if line.startswith("; "):
                pass

            # elif line.startswith("M"):
            #     pass

            # elif line.startswith("M"):
            #     pass


            else:
            
                if 'Z' in line:
                    if New_layer : #If we just changed the layer, we keep the previous value 
                        previous_layer_originZ = previous_Z
                        print(line.split(':'))
                        previous_Z = float(line.split(':')[1])
                        New_layer = False

                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part.startswith("Z"):
                            print(part.split('Z'))
                            Z = float(part.split('Z')[1])
                    
                    if Z == previous_layer_originZ:
                        modified_line = modify_gcode_line(line,previous_current_Z)
                        out_file.write(modified_line + '\n')
                    elif Z == previous_Z:
                        modified_line = modify_gcode_line(line,New_Z_Value)
                        out_file.write(modified_line + '\n')
                    else:
                        modified_line = modify_gcode_line(line,New_Z_Value + 0.122)    
                        out_file.write(modified_line + '\n')
                    
                else: 
                    out_file.write(line)

                
## if we find a new layer, we increase the current layer number 
            if line.startswith(';LAYER_CHANGE'): 
                current_layer += 1
                previous_current_Z = New_Z_Value
                New_Z_Value += layer_height_pattern[(current_layer) % max_nb_pattern]
                New_layer = True


                
if __name__ == "__main__":    
    #We open the gcode
    with open(input_file, 'r') as file:
        code = file.readlines()

    write_new_code(output_file,code)
   
    