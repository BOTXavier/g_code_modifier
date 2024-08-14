# DEfine the patterns of layer's height
layer_height_pattern = {
    0: 0.050,
    1: 0.050,
    2: 0.050,
    3: 0.050,
    4: 0.050,
    5: 0.050,
    6: 0.050,
    7: 0.050,
    8: 0.050,
    9: 0.050,
    10: 0.100,
    11: 0.100,
    12: 0.100,
    13: 0.100,
    14: 0.100,
    15: 0.150,
    16: 0.150,
    17: 0.150
    #4: 0.400
}

layer_flow_pattern = {
    0: 100,
    1: 100,
    2: 100,
    3: 100,
    4: 100,
    5: 100,
    6: 100,
    7: 100,
    8: 100,
    9: 100,
    10: 125,
    11: 125,
    12: 125,
    13: 125,
    14: 125,
    15: 180,
    16: 180,
    17: 180
}


input_file = 'test_05_200.gcode'              # Name of the gfile you want to modify
output_file = 'Modified_2' + input_file     # name of the gfile you want to get after the process.

max_nb_pattern = len(layer_height_pattern)


def modify_gcode_line(line, new_value,flowrate_change_on=False):
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


# def extract_z_origin_value(lines):
#     """
#     This function aims to find the first value of Z in order to start with the accurate value
#     """
    
#     process_began = False

#     for line in lines:
#         #print(line)
#         if process_began:
#             if 'Z' in line:  # ' Z' to ensure we're finding Z as a standalone command
#                 print(line)
#                 if line.startswith(';Z'):
#                     part = line.split(":")
#                     z_value = float(part[1])  # Extract the numeric part of Z
#                     print(z_value)
#                     return z_value
        
#         if line.startswith(';LAYER_CHANGE'):
#             process_began = True
#     return None  # If no Z value is found





def write_new_code(output_file, lines,flowrate_change_on=False):
    current_layer = 0 
    New_Z_Value = 0 #extract_z_origin_value(lines)
    previous_current_Z = 0
    previous_Z = 0
    previous_layer_originZ = 0
    New_layer = False

    
    with open(output_file, 'w') as out_file:
        for line in lines:

            if  flowrate_change_on==True:
                if max_nb_pattern != len(layer_flow_pattern):
                    print("Error : Height and flow patterns are not in the same number")



            if line.startswith("; "):
                out_file.write(line)

            elif line.startswith("M"):
                out_file.write(line)

            

            else:
            
                if 'Z' in line:
                    if New_layer : #If we just changed the layer, we keep the previous value 
                        previous_layer_originZ = previous_Z
                        previous_Z = float(line.split(':')[1])
                        if flowrate_change_on:
                            out_file.write( f"{'M221 S'}{layer_flow_pattern[(current_layer) % max_nb_pattern]}" + '\n')
                        New_layer = False

                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part.startswith("Z"):
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
    
    write_new_code(output_file, code,True)
    print("Gcode modified succesfully")
   
    