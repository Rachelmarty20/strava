__author__ = 'rachel'
__project__ = 'strava'

import cPickle
import time
import sys
import pandas as pd
import datetime
from datetime import date

# might want to import this as an argument
# data_directory = '../../strava/strava/data'


def main(data_directory, segment_name):

    # import data
    efforts, athletes, activities = import_data(data_directory, segment_name)

    # munge
    efforts, athletes, activities = munge(efforts, athletes, activities)

    # combine
    efforts_athletes_activities = combine(efforts, athletes, activities)

    # output to csv
    efforts_athletes_activities.to_csv('{0}/efforts_athletes_activities.{1}.csv'.format(data_directory, segment_name), sep='\t', encoding='utf-8')


def import_data(data_directory, segment_name):
    #efforts_data = cPickle.load(open('{0}/all_efforts.{1}'.format(data_directory, segment_name)))
    #athletes_data_list = [cPickle.load(open('{0}/all_athletes.{1}_{2}'.format(data_directory, segment_name, str(x)))) for x in range(0, 70000, 10000)]
    #activities_data_list = [cPickle.load(open('{0}/all_activities.{1}_{2}'.format(data_directory, segment_name, str(x)))) for x in range(0, 60000, 10000)]

    efforts_data = cPickle.load(open('{0}/all_efforts.{1}'.format(data_directory, segment_name)))
    athletes_data_list = cPickle.load(open('{0}/all_athletes.{1}'.format(data_directory, segment_name)))
    activities_data_list = cPickle.load(open('{0}/all_activities.{1}'.format(data_directory, segment_name)))

    efforts = pd.DataFrame(efforts_data)
    athletes = pd.DataFrame(athletes_data_list)
    activities = pd.DataFrame(activities_data_list)

    return efforts, athletes, activities


def munge(efforts, athletes, activities):

    athletes = athletes.drop_duplicates(keep='last', subset=['created_at', 'username'])
    activities['activities_id'] = activities.loc[:, 'id']
    athletes['athlete_id'] = athletes.loc[:, 'id']

    # adding columns
    efforts['athlete_id'] = efforts['athlete'].apply(get_athlete_id)
    efforts['activities_id'] = efforts['activity'].apply(get_activity_id)
    efforts['athlete_id'] = efforts['athlete'].apply(get_athlete_id)
    efforts['year'] = efforts['start_date_local'].apply(separate_year)
    efforts['month'] = efforts['start_date_local'].apply(separate_month)
    efforts['day'] = efforts['start_date_local'].apply(separate_day)
    efforts['hour'] = efforts['start_date_local'].apply(separate_hour)
    efforts['date'] = efforts['start_date_local'].apply(separate_date)
    efforts['time'] = efforts['start_date_local'].apply(separate_time)
    efforts['weekday'] = efforts['start_date_local'].apply(separate_weekday)
    activities['description_length'] = activities['name'].apply(get_length)

    return efforts, athletes, activities


def combine(efforts, athletes, activities):
    efforts_athletes = pd.merge(efforts, athletes.iloc[3:, :], on='athlete_id', how='left')
    efforts_athletes_activities = pd.merge(efforts_athletes, activities, on='activities_id', how='left')
    efforts_athletes_activities = efforts_athletes_activities[cols]

    efforts_athletes_activities = efforts_athletes_activities[(efforts_athletes_activities['moving_time_x'] < 1000)
                                                          & (efforts_athletes_activities['year'] < 2017)
                                                          & (efforts_athletes_activities['year'] > 2000)
                                                          & (efforts_athletes_activities['moving_time_x'] > 100)]
                                                          #& (efforts_athletes_activities['distance_y'] < 400000)
                                                          #& (efforts_athletes_activities['total_elevation_gain'] < 5000)]
    return efforts_athletes_activities



###########################################  Dataframe functions  #####################################

def get_athlete_id(x):
    return x["id"]
def get_activity_id(x):
    return x["id"]
def separate_weekday(x):
    return date.weekday(datetime.date(int(x.split('-')[0]), int(x.split('-')[1]), int(x.split('-')[2].split('T')[0])))
def separate_year(x):
    return int(x.split('-')[0])
def separate_month(x):
    return int(x.split('-')[1])
def separate_day(x):
    return int(x.split('-')[2].split('T')[0])
def separate_hour(x):
    return int(x.split('T')[1].split(':')[0])
def separate_date(x):
    return x.split('T')[0]
def separate_time(x):
    return x.split('T')[1]
def get_length(x):
    return len(x.split(" "))


cols = ['year', 'month', 'day', 'hour', 'date', 'time', 'weekday', 'description_length',
         u'average_cadence_x',
         u'average_heartrate_x',
         u'distance_x',
         u'elapsed_time_x',
         u'id_x',
         u'max_heartrate_x',
         u'moving_time_x',
         u'start_date_local_x',
         'athlete_id',
         'activities_id',
         u'clubs',
         u'created_at',
         u'firstname',
         u'lastname',
         u'premium',
         u'sex',
         u'state',
         u'username',
         u'athlete_count',
         u'average_cadence_y',
         u'average_heartrate_y',
         u'average_speed',
         u'comment_count',
         u'distance_y',
         u'elapsed_time_y',
         u'id',
         u'kudos_count',
         u'location_city',
         u'max_heartrate_y',
         u'max_speed',
         u'moving_time_y',
         u'name_y',
         u'photo_count',
         u'start_date_local_y',
         u'total_elevation_gain']


###########################################  Main Method  #####################################

if __name__ == "__main__":
    start_time = time.time()
    if len(sys.argv) != 3:
        sys.exit()
    sys.exit(main(sys.argv[1], sys.argv[2]))