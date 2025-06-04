"""
Licensed to YugabyteDB, Inc. under one or more contributor license agreements.
See the NOTICE file distributed with this work for additional information regarding copyright ownership.
YugabyteDB licenses this file to you under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""
import os
import sys
import argparse

def concatenate_yaml_files_with_separator(file_list, output_file):
    with open(output_file, 'w') as outfile:
        for fname in file_list:
            with open(fname) as infile:
                outfile.write('---\n')  # Document separator for YAML
                outfile.write(infile.read())
                outfile.write('\n\n')  # Optional: Adds extra newline for readability

def main():
    parser = argparse.ArgumentParser(description='Concatenate YAML files from a specified directory')
    parser.add_argument('path', nargs='?', default='./', 
                       help='Path to directory containing YAML files (default: current directory)')
    parser.add_argument('-o', '--output', default='concatenated_crd.yaml',
                       help='Output filename (default: concatenated_crd.yaml)')
    
    args = parser.parse_args()
    
    # Validate path exists
    if not os.path.exists(args.path):
        print(f"Error: Path '{args.path}' does not exist")
        sys.exit(1)
    
    if not os.path.isdir(args.path):
        print(f"Error: '{args.path}' is not a directory")
        sys.exit(1)
    
    # Filter to only include .yaml files and create full paths
    yaml_files = []
    for f in os.listdir(args.path):
        if f.endswith('.yaml'):
            yaml_files.append(os.path.join(args.path, f))
    
    # Only proceed if there are YAML files to process
    if yaml_files:
        concatenate_yaml_files_with_separator(yaml_files, args.output)
        print(f"Concatenated {len(yaml_files)} YAML files from '{args.path}' into {args.output}")
    else:
        print(f"No .yaml files found in directory '{args.path}'")

if __name__ == "__main__":
    main()
