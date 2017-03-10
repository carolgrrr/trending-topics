import configparser
from TwitterAPI import TwitterAPI
import sys
import time
import yagmail
from datetime import datetime
from collections import Counter


def get_twitter(config_file):
    """ Read the config_file and construct an instance of TwitterAPI.
    Args:
      config_file ... A config file in ConfigParser format with Twitter credentials
    Returns:
      An instance of TwitterAPI.
    """
    config = configparser.ConfigParser()
    config.read(config_file)
    twitter = TwitterAPI(
                   config.get('twitter', 'consumer_key'),
                   config.get('twitter', 'consumer_secret'),
                   config.get('twitter', 'access_token'),
                   config.get('twitter', 'access_token_secret'))
    return twitter

def robust_request(twitter, resource, params, max_tries=5):
    """ If a Twitter request fails, sleep for 15 minutes.
    Do this at most max_tries times before quitting.
    Args:
      twitter .... A TwitterAPI object.
      resource ... A resource string to request.
      params ..... A parameter dictionary for the request.
      max_tries .. The maximum number of tries to attempt.
    Returns:
      A TwitterResponse object, or None if failed.
    """
    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        else:
            print('Got error:', request.text, '\nsleeping for 15 minutes.', file=sys.stderr)
            sys.stderr.flush()
            time.sleep(61 * 15)

def find_trends(twitter, location):
    topics = robust_request(twitter, 'trends/place', {'id': location}, 20)
    trends = []
    for t in topics:
        topic = "%d\t%s\t%s\t%s\t%s\t%s\n" %(location, t['name'], t['url'], str(t['tweet_volume']), t['promoted_content'], t['query'])
        trends.append(topic)
    return trends

def find_place_ids(twitter):
    places = robust_request(twitter, 'trends/available',{}, 20)
    place_ids = []
    for p in places:
        place_ids.append(p['woeid'])
    return place_ids

def find_places(twitter):
    places = robust_request(twitter, 'trends/available',{}, 20)
    all_places = []
    for p in places:
        all_places.append(p)
    return all_places

def extract_topics(infile, outfile, keyword):
    topics = []
    with open(infile, 'r') as tsv_infile:
        for line in tsv_infile:
            row = line.split()
            if keyword in row[2]:
                topics.append(row)

    topic_counter = count_topics(infile)
    
    with open(outfile, 'w') as tsv_outfile:
        tsv_outfile.write('Location Name\tWOE ID\tName\tURL\tEvents\tPromoted?\tQuery\tCount\n')
        for topic in topics:
            count = topic_counter[topic[2]]
            row = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%d\n" %(topic[0], topic[1], topic[2], topic[3], topic[4], topic[5], topic[6],count)
            tsv_outfile.write(row)

    print('topics filtered.')

def count_topics(filename):
    all_topics = []
    with open(filename, 'r') as topics:
        for line in topics:
            row = line.split()
            all_topics.append(row[2])

    topic_count = Counter(all_topics)
    return topic_count


def email_file(config, filename):
    from_address = config.get('email', 'from')
    password = config.get('email', 'pass')
    to_addresses = config.get('email', 'to')

    contents = ['See attached.', filename]
    email_list = to_addresses.split(',')

    for to_address in email_list:
        yag = yagmail.SMTP(from_address, password)
        yag.send(to_address, filename, contents)
        print('email sent.')

def get_datestring():
    today = datetime.today()
    year, month, day = today.year, today.month, today.day

    if len(str(month)) < 2:
        month = "0%d" %(month)
    else:
        month = "%d" %(month)
    
    if len(str(day)) < 2:
        day = "0%d" %(day)
    else:
        day = "%d" %(day)

    datestring = "%d-%s-%s" %(year, month, day)
    return datestring

def get_trending_topics(filename, place_ids, places, twitter):
    with open(filename, 'w') as tsv_file:
        tsv_file.write('Location Name\tWOE ID\tName\tURL\tEvents\tPromoted?\tQuery\n')

    # iterate through all twitter locations 
    # store trending topics for each location
    for pid in place_ids:
        try:
            trends = find_trends(twitter, pid)
        
            for p in places:
                if p['woeid'] == pid:
                    name = p['name']
            with open(filename, 'a') as tsv_file:
                for topic in trends:
                    tsv_file.write(name+'\t'+ topic)
        except (ConnectionError) as exc:
            print("error: %s" % exc)
            sleep(60*5)
            
def get_top_topics(filename):
    topic_counter = count_topics(filename)
    top_topics = []
    with open(filename, 'r') as topics:
        for line in topics:
            row = line.split('\t')
            loc, woe, name, events, promoted = row[0], row[1], row[2], row[4], row[5]
            count = topic_counter[name]
            top_topics.append((loc, woe, name, events, promoted, count))
    sorted_topics = sorted(top_topics, key=lambda x: (x[5], x[2]), reverse=True)
    top_filename = "top-" + filename
    with open(top_filename, 'w') as tsv_file:
        tsv_file.write('Location Name\tWOE ID\tName\tEvents\tPromoted?\tCount\n')
    
        for topic in sorted_topics:
            if topic[5] > 1:
                row = "%s\t%s\t%s\t%s\t%s\t%s\n" %(topic[0], topic[1], topic[2], topic[3], topic[4], topic[5])
                tsv_file.write(row)

def add_regions(original_file, region_file):
    topics_with_regions = []
    region_list = []
    with open(region_file, 'r') as regions:
        next(regions)
        for line in regions:
            line = line.strip('\n')
            row = line.split(',')
            region_list.append(row)

    with open(original_file, 'r') as topics:
        next(topics)
        for line in topics:
            line = line.strip('\n')
            row = line.split('\t')
            loc = row[0]
            for region in region_list:
                new_loc = region[0]
                if loc == new_loc:
                    row.extend([region[1], region[2], region[3], region[4]])
                    topics_with_regions.append(row)
    
    reg_filename = "regions-and-" + original_file
    with open(reg_filename, 'w') as tsv_file:
        tsv_file.write('Location\tWOE ID\tName\tEvents\tPromoted?\tCount\tLatitude\tLongitude\tNation\tRegion\n')     

        for topic in topics_with_regions:
            #print(topic)
            row = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" %(topic[0], topic[1], topic[2], topic[3], topic[4], topic[5], topic[6], topic[7], topic[8], topic[9])
            tsv_file.write(row)
            
    print("regions added.")



def main():
    config = configparser.ConfigParser()
    config.read('settings.cfg')
    filter_term = config.get('files', 'filter_term')
    prefix = config.get('files', 'prefix')
    twitter = get_twitter('settings.cfg')

    place_ids = find_place_ids(twitter)
    places = find_places(twitter)

    datestring = get_datestring()

    all_topics = prefix + '-' + datestring + '.csv'
    filtered_topics = prefix + '-' + filter_term + '-' + datestring + '.csv'
    top_topics = 'top-' + all_topics

    get_trending_topics(all_topics, place_ids, places, twitter)
    extract_topics(all_topics, filtered_topics, filter_term)
    #email_file(config, filtered_topics)
    get_top_topics(all_topics)
    #email_file(config, top_topics)
    
if __name__ == '__main__':
    main()
    
    