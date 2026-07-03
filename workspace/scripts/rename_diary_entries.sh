#!/bin/bash

# Configuration
DIARY_ROOT="/home/node/.openclaw/workspace/diary/2026"

# Iterate through month directories
for month_dir in "$DIARY_ROOT"/[0-9][0-9]; do
    [ -d "$month_dir" ] || continue
    month=$(basename "$month_dir")
    
    echo "Processing month: $month"
    
    # Iterate through files in the month directory
    for file_path in "$month_dir"/*.md; do
        [ -f "$file_path" ] || continue
        
        filename=$(basename "$file_path")
        
        # Skip files that already match the Lobster convention: YYYY-MM-DD - Day.md
        if [[ "$filename" =~ ^2026-[0-9]{2}-[0-9]{2}\ -\ [a-zA-Z]+\.md$ ]]; then
            echo "Skipping (already correct): $filename"
            continue
        fi
        
        # Skip special strategy files or baks
        if [[ "$filename" == "nathaniel_kitemarking_strategy.md" || "$filename" == *.bak ]]; then
            echo "Skipping (special file): $filename"
            continue
        fi

        # Case 1: Simple numeric names (e.g., 03.md, 17.md)
        if [[ "$filename" =~ ^([0-9]{2})\.md$ ]]; then
            day="${BASH_REMATCH[1]}"
            date_str="2026-$month-$day"
            
            # Use 'date' to get the weekday name
            if day_name=$(date -d "$date_str" +%A 2>/dev/null); then
                new_filename="$date_str - $day_name.md"
                echo "Renaming $filename -> $new_filename"
                mv "$file_path" "$month_dir/$new_filename"
            else
                echo "Error: Could not determine date for $filename"
            fi
            
        else
            echo "Warning: Unrecognized format, skipping: $filename"
        fi
    done
done
