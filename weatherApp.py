import pandas as pd
import requests
import datetime
import jq
import sys

def preprocessing():
    # Kaggle dataset provided in prompt, obtained from https://www.kaggle.com/datasets/viswanathanc/world-cities-datasets
    df = pd.read_csv("worldcities.csv")

    # Converting data types of columns to be used from object type to string type
    df['capital'] = df['capital'].astype('string')
    df['admin_name'] = df['admin_name'].astype('string')

    # Filling NaN values with blank strings
    df['capital'] = df['capital'].fillna('')

    # The following 3 state capitals were not marked as admin in the dataset, making changes after observation
    df.loc[(df['city'] == 'Dover') & (df['admin_name'] == 'Delaware'), 'capital'] = 'admin'
    df.loc[(df['city'] == 'Augusta') & (df['admin_name'] == 'Maine'), 'capital'] = 'admin'
    df.loc[(df['city'] == 'Hartford') & (df['admin_name'] == 'Connecticut'), 'capital'] = 'admin'

    # The following 3 states had more than 1 admin capitals associated with them, making changes so that each state has only 1 capital
    df.loc[(df['city'] == 'Dover') & (df['admin_name'] == 'Pennsylvania'), 'capital'] = ''
    df.loc[(df['city'] == 'Hartford') & (df['admin_name'] == 'South Dakota'), 'capital'] = ''
    df.loc[(df['city'] == 'Augusta') & (df['admin_name'] == 'Georgia'), 'capital'] = ''

    # Filtering the dataset to only get records for USA
    df = df[df['country']=='United States']

    # Dropping nulls and selecting admin capitals for each state
    df = df.dropna(subset=['capital'])
    df = df[df['capital']=='admin']
    df = df.sort_values(by='admin_name')

    # Dataset to assign state_code (Abbreviations) to states, obtained from https://www.kaggle.com/datasets/francescopettini/us-state-names-codes-and-abbreviations?select=state_names.csv
    state_code_df = pd.read_csv('state_names.csv')

    # Merging the 2 datasets and adding the state_code column to original dataset after left join
    df = df.merge(state_code_df[['State', 'Alpha code']], how='left', left_on='admin_name', right_on='State')
    df = df.rename(columns={'Alpha code': 'state_code'})
    df = df.drop(columns=['State'])

    return df

def query_api(df,letter):
    # Identifying all states that begin with the user input and adding their capital, latitude, longitude information to a list as a tuple
    state_matches = df[df['admin_name'].str.startswith(letter)][['state_code', 'city', 'lat', 'lng']].apply(tuple, axis=1).tolist()

    # API key obtained from WeatherAPI
    api_key = "67e9685da4ed488982022959241508"

    # Loop to obtain average temperature for each state match
    for sm in state_matches:
        temperature_list = []
        state = sm[0]
        state_capital = sm[1]
        location = f"{sm[2]},{sm[3]}" # Latitude and longitude values

        # Loop to obtain average temperature in last 5 days
        for i in range(1,6):

            # Calculate the ith date
            date = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
    
            url = "http://api.weatherapi.com/v1/history.json"

            # Query Params for the API GET call, obtained from Swagger specs at https://app.swaggerhub.com/apis-docs/WeatherAPI.com/WeatherAPI/1.0.2#/APIs/history-weather
            params = {
                'key': api_key,
                'q': location,
                'dt': date
            }

            response = requests.get(url, params)
            response_json = response.json()
            
            # Using jq library to extract the average temperature on the particular day
            avg_temp = jq.first('.forecast.forecastday[0].day.avgtemp_f', response_json)
            
            if avg_temp is not None:
                temperature_list.append(avg_temp)

        # Calculate the average temperature over the past days
        average_temperature = sum(temperature_list) / len(temperature_list)

        # Print the result
        print(f"Average temperature over the past {len(temperature_list)} days in {state_capital}, {state}: {average_temperature:.2f}°F")
    print("End of Script")
    sys.exit()


def main():
    letter = ''
    
    # Check if Command-line arguments are valid
    if len(sys.argv) == 2:
        letter = sys.argv[1]
        if letter.isalpha() and len(letter) == 1:
            letter = letter.capitalize()
        else:
            print("Please enter a single letter! Exiting the script")
            sys.exit()
    elif len(sys.argv) > 2:
        print("Too many arguments! Please provide a single letter between A-Z. Exiting the script")
        sys.exit()
    else:
        print("Please provide a letter argument and re-run the script")
        sys.exit()

    # Apply preprocessing to the available datasets
    df = preprocessing()

    # Query the weather API based on the preprocessed dataset and user input
    query_api(df, letter)

if __name__ == "__main__":
    main()