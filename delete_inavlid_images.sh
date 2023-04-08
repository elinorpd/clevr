#!/bin/bash

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --json) json_path="$2"; shift ;;
    --dir) dir_path="$2"; shift ;;
    *) echo "Unknown parameter: $1"; exit 1 ;;
  esac
  shift
done

# Check if JSON and directory paths were provided
if [[ -z "$json_path" ]]; then
  echo "Please provide a path to the JSON file with the --json flag."
  exit 1
fi
if [[ -z "$dir_path" ]]; then
  echo "Please provide a path to the directory with the --dir flag."
  exit 1
fi

# Load the JSON file and extract the keys
keys=$(jq -r 'keys[]' "$json_path")

# Initialize counters
deleted=0
remaining=0

# Loop through the directory's files and delete any that are not in the JSON
for file in "$dir_path"/*; do
  # Extract the filename without the extension
  filename=$(basename "$file" | cut -f 1 -d '.')

  # Check if the filename is not in the JSON
  if [[ ! $keys =~ $filename ]]; then
    # echo "Deleting $file"
    # rm "$file"
    ((deleted++))
  else
    ((remaining++))
  fi
done

echo "Deleted $deleted file(s)."
echo "Remaining $remaining file(s)."