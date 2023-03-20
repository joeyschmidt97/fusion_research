import os

print('Test')
# Check if file exists
if os.path.isfile('out.neo.run'):
    
    # Create empty dictionary
    info_dict = {}

    # Open file and read lines
    with open('out.neo.run', 'r') as f:
        lines = f.readlines()

    # Loop through lines
    for line in lines:

        # Ignore lines that don't contain a colon
        if ':' not in line:
            continue

        print(line)
        # Split line at the colon
        key, value = line.split(':')

        # Strip whitespace from key and value
        key = key.strip()
        value = value.strip()

        # Convert numerical values to floats
        if value.replace('.', '', 1).isdigit():
            value = float(value)

        # Add key-value pair to dictionary
        info_dict[key] = value

    # Print resulting dictionary
    print(info_dict)

else:
    print('File not found.')
