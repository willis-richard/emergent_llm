#!/bin/bash

# Set the source directory and destination directory
SOURCE_DIR="results"
DEST_DIR="copied_diagrams"  # Change this to your desired destination

# Create destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Find all social_welfare.png files and process them
find "$SOURCE_DIR" -name "social_welfare.png" -type f | while read -r file; do
    # Extract the path components
    # file will be like: results/game_name/provider_model/batch_mixture/social_welfare.png

    # Get the relative path from results/
    rel_path="${file#$SOURCE_DIR/}"

    # Extract game name (first directory after results/)
    game=$(echo "$rel_path" | cut -d'/' -f1)

    # Extract provider_model (second directory)
    provider_model=$(echo "$rel_path" | cut -d'/' -f2)

    # Extract just the model part (everything after the first underscore)
    model="${provider_model#*_}"

    # Create new filename
    new_name="${game}_${model}_social_welfare.png"

    # Copy and rename
    cp "$file" "$DEST_DIR/$new_name"

    echo "Copied: $file -> $DEST_DIR/$new_name"
done

echo "Done! All files copied to $DEST_DIR"
