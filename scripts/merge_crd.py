import os 
def concatenate_yaml_files_with_separator(file_list, output_file):
    with open(output_file, 'w') as outfile:
        for fname in file_list:
            with open(fname) as infile:
                outfile.write('---\n')  # Document separator for YAML
                outfile.write(infile.read())
                outfile.write('\n\n')  # Optional: Adds extra newline for readability

# List your YAML files here
yaml_files = os.listdir("./") 
output_yaml = 'concatenated_crd.yaml'

concatenate_yaml_files_with_separator(yaml_files, output_yaml)
