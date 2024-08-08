#!/bin/bash

# Check if a directory is provided as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 <directory>"
  exit 1
fi

# Function to rename directories
rename_dirs() {
  local dir="$1"

  # Traverse the directory tree
  find "$dir" -depth -type d | while read -r old_dir; do
    new_dir=$(echo "$old_dir" | sed 's/_/:/g')
    if [ "$old_dir" != "$new_dir" ]; then
      mv "$old_dir" "$new_dir"
      echo "Renamed: $old_dir -> $new_dir"
    fi
  done
}

# Call the function with the provided directory
rename_dirs "$1"
