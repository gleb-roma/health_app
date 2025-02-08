
import pandas as pd
import xml.etree.ElementTree as ET

# ---------------------------
# Parse the workouts from export.xml
# ---------------------------

# Parse the XML file (export.xml)
tree = ET.parse('apple_health_export-2/export.xml')
print("Parsed export.xml file")
root = tree.getroot()

# Extract Workout elements and their details
workouts = []
for workout in root.findall('Workout'):
    # Get attributes from the Workout element.
    activity = workout.get('workoutActivityType')
    duration = workout.get('duration')
    total_distance = workout.get('totalDistance')
    total_energy = workout.get('totalEnergyBurned')
    start_date = workout.get('startDate')
    end_date = workout.get('endDate')
    
    # Construct a record, converting numeric values where possible
    workout_data = {
        'activity': activity,
        'duration': float(duration) if duration else None,
        'total_distance': float(total_distance) if total_distance else None,
        'total_energy': float(total_energy) if total_energy else None,
        'start_date': start_date,
        'end_date': end_date
    }
    workouts.append(workout_data)

# Convert the list of workouts to a DataFrame
df_workouts = pd.DataFrame(workouts)

# Display the first few rows of the DataFrame
print("Workouts DataFrame preview:")
print(df_workouts.head())

# Display the frequencies of each activity type
print("\nWorkout Activity Frequencies:")
print(df_workouts['activity'].value_counts())

# Save the workouts DataFrame to a Parquet file with snappy compression
df_workouts.to_parquet('activities_data_2.parquet', compression='snappy')
print("\nWorkouts DataFrame saved to activities_data.parquet")