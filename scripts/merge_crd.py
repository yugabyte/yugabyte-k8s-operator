"""
Licensed to YugabyteDB, Inc. under one or more contributor license agreements.  
See the NOTICE file distributed with this work for additional information regarding copyright ownership. 
YugabyteDB licenses this file to you under the Apache License, Version 2.0 (the "License"); 
you may not use this file except in compliance with the License.  
You may obtain a copy of the License ag http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""


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
