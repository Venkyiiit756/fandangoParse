import pandas as pd
import re
import datetime

# File path (assuming the file is passed from the Node.js app)
file_path = 'aug22_2055.txt'

# Read the content of the file
with open(file_path, 'r') as file:
    content = file.read()

# Extract the data using regex
pattern = r"url: '(.+?)',\s+availableSeats: (\d+),\s+totalSeats: (\d+)"
matches = re.findall(pattern, content)

# Create a list of dictionaries for each match
data = []
for i, match in enumerate(matches, start=1):
    url, available_seats, total_seats = match
    booked_seats = int(total_seats) - int(available_seats)
    occupancy = (booked_seats / int(total_seats)) * 100
    theater_id = re.search(r'tid=(.+?)&', url).group(1)
    show_time = re.search(r'sdate=(.+?)&', url).group(1).replace('%2B', ' ')
    
    data.append({
        's.no': i,
        'theater id': theater_id,
        'show time': show_time,
        'total seats': total_seats,
        'available seats': available_seats,
        'booked seats': booked_seats,
        'occupancy': occupancy
    })

# Create DataFrame
df = pd.DataFrame(data)

# Add a total row for sum of seats and average occupancy
total_row = pd.DataFrame([{
    's.no': 'Total',
    'theater id': '',
    'show time': '',
    'total seats': df['total seats'].astype(int).sum(),
    'available seats': df['available seats'].astype(int).sum(),
    'booked seats': df['booked seats'].sum(),
    'occupancy': df['occupancy'].mean()
}])

# Use concat instead of append
df = pd.concat([df, total_row], ignore_index=True)

# Save the DataFrame to an Excel file
# Get the current date and time
current_datetime = datetime.datetime.now()

# Format the date and time as a string
timestamp = current_datetime.strftime("%Y%m%d_%H%M%S")

# Create the excel file name with the timestamp as a suffix
excel_path = f"theater_data_{timestamp}.xlsx"

# Save the DataFrame to an Excel file
df.to_excel(excel_path, index=False)

print(f"Excel file created at: {excel_path}")

