#!/bin/bash

# Base directory where wavs/ folder is located
base_dir="./data/porameht_voice_th169k"

# Function to calculate total duration for a split
calculate_duration() {
    metadata_file="$1"
    split_name="$2"
    total_seconds=0

    while IFS='|' read -r audio_file transcript; do
        # Skip header
        if [[ "$audio_file" == "audio_file" ]]; then continue; fi

        # Full path to the wav file
        full_path="${base_dir}/${audio_file}"

        # Check if file exists
        if [[ ! -f "$full_path" ]]; then
            echo "Warning: File not found: $full_path"
            continue
        fi

        # Get duration and check if it's a number
        duration=$(soxi -D "$full_path" 2>/dev/null)
        if [[ "$duration" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
            total_seconds=$(echo "$total_seconds + $duration" | bc)
        else
            echo "Warning: Could not get duration for $full_path"
        fi
    done < "$metadata_file"

    total_hours=$(echo "$total_seconds / 3600" | bc -l)
    printf "%s: %.2f hours\n" "$split_name" "$total_hours"
}

# Run for each metadata CSV
calculate_duration "${base_dir}/train_metadata.csv" "Train"
calculate_duration "${base_dir}/dev_metadata.csv" "Dev"
calculate_duration "${base_dir}/test_metadata.csv" "Test"