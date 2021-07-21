

Setup:
-Create a folder for the project
-Create a virtual environment i.e. virtualenv env at command line (must be done in your project directory)
-Activate virtualenv:  From project folder in cmd, cd env/scripts. type activate.  cd ../.. to get back to project root 
-Load libraries: pip install requirements.txt

To run the program:
python noaa1.py

Program Features:
Automatically determines your location using your public IP
Uses several NOAA api endpoint to determine:
- Alerts (severe weather and alerts for your state)
- Tide Data/Forecast
- Weather Forecast
- Grid Data
- Writes JSON String data to files in the root folder of your project (you can view these to see the data structure)

Future Releases:
- Incorporate email of data to target user
- Output of combined/processed data to a single file
- Addition of more detailed weather data from non-NOAA apis
- Addition of Solunar Data