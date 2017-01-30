__author__ = 'rachel'
__project__ = 'strava'

import requests
import cPickle
import time
import sys
import pandas as pd
reload(sys)
sys.setdefaultencoding('utf8')

access_token = 'c5335434a1f7d482a47507f064ad6f9e6dec3a76'
extra_headers = {'Authorization' : 'Bearer %s' % access_token}
api_base_url = 'https://www.strava.com/api/v3/'
per_page = 200 # Strava max

# find an alternative way to download if still  nothing by tomorrow (01/18) morning...

def main():

    get_segment_efforts()

    # can maybe change
    fnames = ['data/all_efforts.Mission_Bay_South', 'data/all_efforts.The_Ouchey_Flat']
    segment_names = ['Mission_Bay_South', 'The_Ouchey_Flat']

    for i in range(1):
        fname = fnames[i]
        segment_name = segment_names[i]
        print segment_name

        athletes, activities = import_segment(fname)

        get_athletes(athletes, segment_name)

        get_activities(activities, segment_name)

def import_segment(fname):
    '''
    Get the athlete and activity information from the segments
    :param fname: all efforts file for a segment
    :return: lists of athletes and activities
    '''

    segment_dict = cPickle.load(open(fname))
    all_efforts_df = pd.DataFrame(segment_dict)

    # should really have reduced this to a set!!!
    athletes = [x["id"] for x in all_efforts_df['athlete']]
    activities = [x["id"] for x in all_efforts_df['activity']]

    return athletes, activities


def get_segment_efforts():

    # url paths
    api_segment_url = api_base_url + 'segments/%d'
    api_segment_all_efforts_url = api_segment_url + '/all_efforts'

    # segment assignments
    segment_ids = [915551, 3858425]
    segment_names = ['Mission_Bay_South', 'The_Ouchey_Flat']


    for i, segment_id in enumerate(segment_ids[:1]):
        segment_name = segment_names[i]
        print segment_name

        all_efforts_fname = 'data/all_efforts.%s' % segment_name

        all_efforts = []
        r = requests.get(api_segment_url % segment_id, headers=extra_headers)
        n_efforts = r.json()['effort_count']
        sys.stdout.write('Fetching all %d effort summaries for segment %d\n' % (n_efforts, segment_id))
        for i in range(1, 2 + n_efforts / per_page):
            sys.stdout.write('Making summary request %d\n' % i)
            r = requests.get(api_segment_all_efforts_url % segment_id, headers=extra_headers, params={'per_page' : per_page, 'page' : i})
            if r.status_code != 200:
                sys.stderr.write('Error, received code %d for summary request %d\n' % (r.status_code, i))
            else:
                all_efforts.extend(r.json())
            time.sleep(2) # Make sure do not hit Strava rate limiting
        cPickle.dump(all_efforts, open(all_efforts_fname, 'w'))


def get_athletes(athletes, segment_name):

    # test this in small scale in notebook to see what fails???

    all_athletes_fname = 'data/all_athletes.%s' % segment_name
    api_athlete_url = api_base_url + 'athletes/%d'

    all_athletes = []
    sys.stdout.write('Total number of athletes: %d\n' % len(athletes))

    for i, athlete_id in enumerate(athletes):
        sys.stdout.write('Making summary request %d\n' % i)
        r = requests.get(api_athlete_url % athlete_id, headers=extra_headers)
        if r.status_code != 200:
            sys.stderr.write('Error, received code %d for summary request %d\n' % (r.status_code, i))
        else:
            all_athletes.append(r.json())
        time.sleep(2) # Make sure do not hit Strava rate limiting
    cPickle.dump(all_athletes, open(all_athletes_fname, 'w'))


def get_activities(activities, segment_name):

    all_activities_fname = 'data/all_activities.%s' % segment_name
    api_activities_url = api_base_url + 'activities/%d'

    all_activities = []
    sys.stdout.write('Total number of activities: %d\n' % len(activities))

    for i, activities_id in enumerate(activities):
        sys.stdout.write('Making summary request %d\n' % i)
        r = requests.get(api_activities_url % activities_id, headers=extra_headers)
        if r.status_code != 200:
            sys.stderr.write('Error, received code %d for summary request %d\n' % (r.status_code, i))
        else:
            all_activities.append(r.json())
        time.sleep(2) # Make sure do not hit Strava rate limiting
    cPickle.dump(all_activities, open(all_activities_fname, 'w'))



###########################################  Main Method  #####################################

if __name__ == "__main__":
    start_time = time.time()
    if len(sys.argv) != 1:
        sys.exit()
    sys.exit(main())
