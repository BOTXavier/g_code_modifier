input_file = 'test.gcode'              # Name of the gfile you want to modify
output_file = 'Modified_' + input_file     # name of the gfile you want to get after the process.


# DEfine the patterns of layer's height
layer_height_pattern = {

}


#good combos : 0.05/85 ; 0.100/130 ; 0.150/185
layer_flow_pattern = {

}

# for i in range(36):
#     if i < 6: 
#         layer_height_pattern[i] = 0.05
#         layer_flow_pattern[i] = 85
#     elif i < 12:
#         layer_height_pattern[i] = 0.100
#         layer_flow_pattern[i] = 130
#     elif i < 18:
#         layer_height_pattern[i] = 0.150
#         layer_flow_pattern[i] = 180
#     elif i < 24:
#         layer_height_pattern[i] = 0.200
#         layer_flow_pattern[i] = 190
#     elif i < 30:
#         layer_height_pattern[i] = 0.250
#         layer_flow_pattern[i] = 210
#     elif i < 36:
#         layer_height_pattern[i] = 0.300
#         layer_flow_pattern[i] = 210

for i in range(140):
    if i < 100: 
        layer_height_pattern[i] = 0.05
        layer_flow_pattern[i] = 85
    else:
        layer_height_pattern[i] = 0.150
        layer_flow_pattern[i] = 185


print(layer_height_pattern)
print(layer_flow_pattern)
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
    previous_current_Z = 0 # Z of this layer before the code was modified
    previous_Z = 0 # Z before the code was modified
    previous_layer_originZ = 0 # Z of the layer before the one we are currently, from before the modifications
    New_layer = False # have we entered a new layer or not 

    if  flowrate_change_on==True: ## Check if the two patterns are matching
            if max_nb_pattern != len(layer_flow_pattern):
                print("Error : Height and flow patterns are not in the same number")
    
    with open(output_file, 'w') as out_file: #Open the writing file 
        for line in lines: 

            if line.startswith("; "): # then those are comments, no need to modify them, nor even to write them
                out_file.write(line)

            elif line.startswith("M"): # Then those are parameters that we don't want to change neither
                out_file.write(line)

            else:
            
                if 'Z' in line: # we gotta modify it
                    if New_layer : #If we just changed the layer, we keep the previous value 
                        previous_layer_originZ = previous_Z
                        previous_Z = float(line.split(':')[1]) # we read the comment line stating the current Z

                        if flowrate_change_on:
                            new_flow_rate = layer_flow_pattern[(current_layer) % max_nb_pattern]
                            out_file.write( f"{';Layer number:'}{current_layer}" + '\n')  # Add a comment
                            out_file.write( f"{';New Layer Height:'}{layer_height_pattern[(current_layer) % max_nb_pattern]}" + '\n')  # add a comment
                            out_file.write( f"{';New Z:'}{New_Z_Value}" + '\n') # add a comment 
                            out_file.write( f"{'M221 S'}{new_flow_rate}" + '\n') # change the flowrate for this new layer
#                            out_file.write( f"{'G4 P'}{500}" + '\n') # This line adds a 500µs break 

                            
                        New_layer = False # we entered the new layer

                    parts = line.split() # we want to find the part of the line where we have to modify the Z

                    for part in parts:
                        if part.startswith("Z"):
                            Z = float(part.split('Z')[1]) # we read what Z is written to know what modification to do
                            break
                    
                    if Z == previous_layer_originZ:
                        modified_line = modify_gcode_line(line,previous_current_Z)
                        out_file.write(modified_line + '\n')
                    elif Z == previous_Z:
                        modified_line = modify_gcode_line(line,New_Z_Value)
                        out_file.write(modified_line + '\n')
                    else:
                        modified_line = modify_gcode_line(line,New_Z_Value + 0.122) #0.122 chosed arbitrarily after reading the code   
                        out_file.write(modified_line + '\n') 
                    
                else: 
                    out_file.write(line)

                
## if we find a new layer, we increase the current layer number 
            if line.startswith(';LAYER_CHANGE'): 
                current_layer += 1
                previous_current_Z = New_Z_Value
                new_height = layer_height_pattern[(current_layer) % max_nb_pattern]
                New_Z_Value += new_height
                New_layer = True


                
if __name__ == "__main__":    
    #We open the gcode
    with open(input_file, 'r') as file:
        code = file.readlines()
    
    write_new_code(output_file, code,True)
    print("Gcode modified succesfully")
   
    