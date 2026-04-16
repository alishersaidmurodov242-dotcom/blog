#!/usr/bin/env python
# Quick script to remove orphaned code from models.py

path = r'd:\NajotTalim\uy_ishi_1\blog\models.py'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and remove the orphaned lines (around line 123-125)
# We're looking for lines that contain "output_size" at indentation level 12 spaces
new_lines = []
skip_next = 0

for i, line in enumerate(lines):
    if skip_next > 0:
        skip_next -= 1
        continue
    
    # Check if this is one of the orphaned lines (12 spaces + "output_size")
    if line.strip() == 'output_size = (300, 300)' and line.startswith('            output_size'):
        # Skip this line and the next 2 lines (img.thumbnail and img.save)
        skip_next = 2
        continue
    
    new_lines.append(line)

# Also remove the blank line before if the next line was skipped
final_lines = []
for i, line in enumerate(new_lines):
    if i < len(new_lines) - 1:
        # Check if current is blank and next starts with output_size at wrong level
        if line.strip() == '' and i > 0 and new_lines[i-1].strip() == 'pass':
            # Check if there's any non-blank content after this blank line
            has_content = False
            for j in range(i+1, len(new_lines)):
                if new_lines[j].strip():
                    if new_lines[j].strip().startswith('output_size'):
                        continue
                    has_content = True
                    break
            if not has_content or (i+1 < len(new_lines) and new_lines[i+1].strip().startswith('output_size')):
                continue
    final_lines.append(line)

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(final_lines)

print('Fixed models.py - removed orphaned code')
