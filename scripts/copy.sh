#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Error: Exactly 2 arguments required" >&2
    echo "Usage: $0 <arg1> <arg2>" >&2
    exit 1
fi

if [ ! -e "$1" ]; then
    echo "Error: Path '$1' does not exist" >&2
    exit 1
fi

if [ ! -e "$2" ]; then
    echo "Error: Path '$2' does not exist" >&2
    exit 1
fi

SOURCE_DIR=$1
DEST_DIR=$2

DIAGRAMS=("social_welfare.svg" "schelling_n_16.svg")

for diagram in "${DIAGRAMS[@]}"; do
    find "$SOURCE_DIR" -name $diagram -type f | while read -r file; do
        # Extract the path components
        # file will be like: results/game_name/provider_model/batch_mixture/social_welfare.png
        # Get the relative path from SOURCE_DIR/
        rel_path="${file#${SOURCE_DIR%/}/}"

        # Extract game name (first directory after results/)
        game=$(echo "$rel_path" | cut -d'/' -f1)

        # Extract provider_model (second directory)
        provider_model=$(echo "$rel_path" | cut -d'/' -f2)

        # Extract just the model part (everything after the first underscore)
        model="${provider_model#*_}"

        # Create new filename
        new_name="${game}_${model}_${diagram}"

        # Copy and rename
        cp "$file" "$DEST_DIR/$new_name"

        echo "Copied: $file -> $DEST_DIR/$new_name"
    done
done
