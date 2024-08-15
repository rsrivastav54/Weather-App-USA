# Weather-App-USA
A weather app that shows average temperature in the last 5 days from capital cities of US states

# Steps to run
## From Github:
1. Clone the repository 
2. cd into the directory
3. Install requirements using 'pip install -r requirements.txt'
4. Run the app using 'python weatherApp.py [Capital/Small Alphabet of State]', ex. 'python weatherApp.py M'
5. Script returns average temperature over the last 5 days for capital cities of all matching States according to user input

## Using Docker:
1. Clone the repository
2. cd into the directory
3. Use 'docker build -t weather-app . ' to build the image 
4. Run the app container using 'docker run weather-app [Capital/Small Alphabet of State]', ex. 'docker run weather-app M'
5. Script returns average temperature over the last 5 days for capital cities of all matching States according to user input