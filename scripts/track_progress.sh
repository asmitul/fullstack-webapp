#!/bin/bash

# Create the scripts directory if it doesn't exist
mkdir -p $(dirname "$0")

# Function to count completed and total tasks
count_tasks() {
    local file=$1
    local total=$(grep -c "\- \[ \]" "$file")
    local completed=$(grep -c "\- \[x\]" "$file")
    local total_all=$((total + completed))
    local percent=0
    
    if [ $total_all -gt 0 ]; then
        percent=$(( (completed * 100) / total_all ))
    fi
    
    echo "File: $file"
    echo "  Completed: $completed / $total_all tasks ($percent%)"
    echo ""
}

# Print header
echo "=========================================="
echo "Task Management Web Application - Progress"
echo "=========================================="
echo ""

# Check if TODO.md exists
if [ -f "TODO.md" ]; then
    count_tasks "TODO.md"
else
    echo "TODO.md not found!"
    echo ""
fi

# Check if NEXT_SPRINT.md exists
if [ -f "NEXT_SPRINT.md" ]; then
    count_tasks "NEXT_SPRINT.md"
else
    echo "NEXT_SPRINT.md not found!"
    echo ""
fi

# Count tasks by category in TODO.md
if [ -f "TODO.md" ]; then
    echo "Progress by Category:"
    echo "--------------------"
    
    # Define categories to search for
    categories=("Immediate Tasks" "Backend Enhancements" "Frontend Enhancements" "DevOps & Infrastructure" "Documentation" "Testing" "Future Features" "Maintenance")
    
    for category in "${categories[@]}"; do
        # Find the line number where the category starts
        start_line=$(grep -n "^## $category" TODO.md | cut -d: -f1)
        
        if [ ! -z "$start_line" ]; then
            # Extract tasks for this category
            category_content=$(sed -n "$start_line,/^## /p" TODO.md | grep -v "^## ")
            
            # Count tasks
            total=$(echo "$category_content" | grep -c "\- \[ \]")
            completed=$(echo "$category_content" | grep -c "\- \[x\]")
            total_all=$((total + completed))
            percent=0
            
            if [ $total_all -gt 0 ]; then
                percent=$(( (completed * 100) / total_all ))
            fi
            
            echo "  $category: $completed / $total_all tasks ($percent%)"
        fi
    done
fi

echo ""
echo "==========================================" 