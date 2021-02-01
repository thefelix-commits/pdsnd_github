import time
import pandas as pd
import numpy as np
#from matplotlib import pyplot as plt

#Definition of Filters
CITY_DATAS = { 'c': ['Chicago', 'chicago.csv'],
               'n': ['New York City', 'new_york_city.csv'],
               'w': ['Washington', 'washington.csv'] }

MONTH_DATAS = { '1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May', '6': 'June',
                '7': 'July', '8': 'August', '9': 'september', '10': 'October', '11': 'November', '12': 'December', 'a': 'All'}

DAY_DATAS = {'1': 'Monday', '2': 'Tuesday', '3': 'Wednesday', '4': 'Thursday', '5': 'Friday', '6': 'Saturday', '7': 'Sunday', 'a': 'All'}

#Setting, how many lines will be shown at all analysis with "Top x" questions
top = 5

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze. 
    Returns:
        (str) city - initial of the name of the city to analyze (as we have only three datasets so far)
        (str) month - number of the month to filter by, or "all" to apply no month filter
        (str) day - number of the day of week to filter by, or "all" to apply no day filter
    """
    print('### START ANALYSIS ###')
    print('Hello! Let\'s explore some US bikeshare data!')
    
    #Select CITY
    cityf = None    
    print('Which city\'s dataset are you interested in? Press first letter of cities name as in brackets. Available data: ')
    #Print available cities
    for key in CITY_DATAS:
        cty = CITY_DATAS[key]
        print('(' + key + ') ' + cty[0] + "   ", end='')
    #Get users choice
    while cityf is None: 
        town = input('Enter which city: ')  #get input for city
        town = town.lower()
        cityf = CITY_DATAS.get(town)
        if cityf is None:
            print('This selection is not available, please use another selection.')
    print('You chose: ' + cityf[0] + '  // short: ' + town)
    
    #Select MONTH
    monthf = None
    print('\nWhich month (1-12) would you like to evaluate? (type 1 - 12 or \'a\' for all).')
    #Print available months
    for key in MONTH_DATAS:
        print('(' + key + ') ' + MONTH_DATAS.get(key) + "  ", end='')    
    #Get users choice
    while monthf is None: 
        mon = str(input('Month: '))  #get input for month
        mon = mon.lower()
        monthf = MONTH_DATAS.get(mon)
        if monthf is None:
            print('This selection is not available, please use another selection.')
    print('You chose: ' + monthf)
    
    #Select DAY
    dayf = None
    print()
    print('\nWhich day of the week (1-7) would you like to evaluate? (type 1 - 12 or \'a\' for all).')
    #Print available days
    for key in DAY_DATAS:
        print('(' + key + ') ' + DAY_DATAS.get(key) + "  ", end='')    
    #Get users choice
    while dayf is None: 
        da = str(input('Day: '))  #get input for day
        da = da.lower()
        dayf = DAY_DATAS.get(da)
        if dayf is None:
            print('This selection is not available, please use another selection.')
    print('You chose: ' + dayf)
    
    print('-'*40)
    # RESTRUCTURE to TOWN
    return town, mon, da


def load_data(cityl, monthl, dayl):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - initial of the city to analyze
        (str) month - number of the month to filter by, or "all" to apply no month filter
        (str) day - number of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df3 - Pandas DataFrame containing city data reduced to selected month and day
    """
    
    #load csv file content into dataframe
    print('### LOAD DATA ###')
    print('Loading file: ' + CITY_DATAS.get(cityl)[1])
    df = pd.read_csv('./' + CITY_DATAS.get(cityl)[1])
    
    #convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
   
    #reduce to relevant month, put in df2
    if monthl != 'a':
        df_month = df[df["Start Time"].dt.month == int(monthl)]
    else:
        df_month = df

    # reduce to relevant day, put in df3
    if dayl != 'a':
        df_day = df_month[df_month["Start Time"].dt.day == int(dayl)]
    else:
        df_day = df_month
    print('-'*40)

    return df_day


def time_stats(dfx,  month_filter, day_filter):
    """
    Some statistics about time (most common month, day of week, hours)
    Args:    dfx - Array of Bike Sharing data
    Returns: none - only internal prints
    """
    print('----- Most popular month/day/hours -----') #explanation, what is done 
    start_time = time.time()

    #month
    #popular_month = df['Start Time'].dt.month.mode()[0]
    popular_month = dfx['Start Time'].dt.month.value_counts()   #I used value_counts instead of mode
    if month_filter == 'a':
        print('month-rentals (Top ' + str(top) + ')')
    else:
        print('\nOnly ' + str(MONTH_DATAS[str(month_filter)]) + ' was selected.')
        print('month-rentals')
    print(popular_month[:top])

    #day of week
    popular_days = dfx['Start Time'].dt.day.value_counts() 
    if day_filter == 'a':
        print('\nday--rentals (Top ' + str(top) + ')')
    else:
        print('\nOnly ' + str(DAY_DATAS[str(day_filter)]) + ' was selected.') 
        print('day--rentals   (day=day of week)')
    print(popular_days[:top])  
    
    #hours
    popular_hours = dfx['Start Time'].dt.hour.value_counts()   
    print('\nhour--rentals (Top ' + str(top) + ')')
    print(popular_hours[:top])  
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def station_stats(dfx):
    """
    Some statistics about stations (most common start, end, and relation from start to end)
    Args:    dfx - Array of Bike Sharing data
    Returns: none - only internal prints
    """    

    print('----- Most popular stations (Top ' + str(top) + ') ----')   
    start_time = time.time()

    # find the top x start stations
    popular_st_start = dfx['Start Station'].value_counts()
    print('\nMost popular start stations (Top ' + str(top) + '):')
    print(popular_st_start[:top])
    
    # find the top x end stations
    popular_st_end = dfx['End Station'].value_counts()
    print('\nMost Popular End Stations (Top ' + str(top) +'):')
    print(popular_st_end[:top])   
    
    # find the top combination of start and end stations
    dfx['Start End Station'] = 'Start: ' + dfx['Start Station'] + '   End: ' + dfx['End Station']
    popular_st_start_end = dfx['Start End Station'].value_counts()
    print('\nMost Popular Relations (Top ' + str(top) +'):')
    print(popular_st_start_end[:top])   
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def trip_duration_stats(dfx):
    """
    Some statistics about trip duration (monthly sum, mean)
    Args:    dfx - Array of Bike Sharing data
    Returns: none - only internal prints
    """    
    print('------ Analysis on trip duration -------\n')   
    start_time = time.time()

    #display total travel time, 2 decimal places
    total_travel = dfx['Trip Duration'].sum()
    print('Total travel Time (hours): %.2f\n' % (total_travel/3600))

    #display mean travel time, 2 decimal places
    mean_travel = dfx['Trip Duration'].mean()
    print('Mean travel Time (minutes): %.2f' % (mean_travel/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def user_stats(dfx):
    """
    Some statistics about users (type, distribution of gender and age)
    Args:    df - Array of Bike Sharing data
    Returns: none - only internal prints
    """
    print('-------------- User stats --------------\n')   
    start_time = time.time()

    #Display counts of user types
    user_types = dfx['User Type'].value_counts()
    print('User types of subscription:')
    print(user_types[:top])   

    #Display counts of gender
    try: 
        user_gender = dfx['Gender'].value_counts()
        print('\nGender of users:')
        print(user_gender[:top]) 
    except:
        print('Column/data "gender" not included in data of selected city.')

    #Display earliest, most recent, and most common year of birth. Print approx. age
    try:
    	now = time.gmtime()
        birth = dfx['Birth Year'].min()
        print('\nBirth (Min.) ' + str(birth)[0:4] + '   (approx. age.: ' + str(now[0] - birth) + ')') 
        birth = dfx['Birth Year'].max()
        print('Birth (Max.): ' + str(birth)[0:4] + '   (approx. age.: ' + str(now[0] - birth) + ')') 
        birth = dfx['Birth Year'].mode()[0]
        print('Birth (Most years occuring in dataset): ' + str(birth)[0:4] + '   (approx. age.: ' + str(now[0] - birth) + ')')
    except:
        print('Column/data "birthdate" not included in data of selected city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def show_raw_data(dfx):
    """
    Show raw_data on users demand. In steps of 5 lines
    Args:    dfx - array of Bike Sharing data (already filtered on month and day)
    Returns: none - only internal prints
    """
    more = 'y'
    i = 0
    while more == 'y':           
        print(dfx[i*5:((i+1)*5)])            #print 5 lines
        more = input('See more data (y): ')  #ask user for demand of further lines
        i += 1
        if len(dfx) <= (i+1)*5:
            break
    print('Raw data check ends here.')
    
    
def main():
    while True:
        city, month, day = get_filters() #get user input, which datasets should be analysed
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        print('\nIf you like to check raw data, please press (r).')
        restart = input('Would you like to restart? Enter (y) yes or (n) no.\n')
        if restart.lower() != 'yes' and restart.lower() != 'y' and restart.lower() != 'r':
            print('Thank you for using this analysis. For feedback do not hesitate to contact us')
            break
        if restart.lower() == 'r':
            show_raw_data(df)
        

if __name__ == "__main__":
    main()