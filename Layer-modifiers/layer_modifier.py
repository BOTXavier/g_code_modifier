# Définir le motif des layer's height
flow_rate_pattern = {
    0: 0.200,
    1: 0.250,
    2: 0.300,
    3: 0.350,
    4: 0.400
}

# Lire le fichier G-code
input_file = 'test.gcode'
output_file = 'testModified.gcode'

with open(input_file, 'r') as file:
    lines = file.readlines()

current_layer = 0

# Écrire le nouveau fichier G-code
with open(output_file, 'w') as new_file:
    for line in lines:
        if line.startswith(';LAYER:'):
            current_layer = int(line.split(':')[1])
            # Vérifier si on est dans les couches cibles
            if current_layer >= 5 and current_layer <= 50:
                pattern_layer = (current_layer) % 5  # Calculer la position dans le motif
                if pattern_layer in flow_rate_pattern:
                    height = flow_rate_pattern[pattern_layer]
                    new_file.write(f';Layer height:{height}\n')
        new_file.write(line)