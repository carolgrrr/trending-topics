from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
import configparser


### DATA PREP FUNCTIONS ###

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

def sort_by_trend_count(tsv):
    today = get_datestring()
    rows = []

    for row in tsv:
        if not fileinput.isfirstline():
            cells = row.split('\t')
            if cells[0] == today:
                del(cells[0])
                rows.append(cells)

    for row in rows:
        #if row == rows[0]:
        #    continue
        row[5] = int(row[5])

    # x[5] = count x[2] = trend, x[0] = location, x[8] = nation, x[9] = region
    sorted_rows = sorted(rows, key = lambda x: (-x[5], x[2], x[9], x[8], x[0]))
    return sorted_rows

def sort_by_location(tsv):
    today = get_datestring()
    rows = []

    for row in tsv:
        if not fileinput.isfirstline():
            cells = row.split('\t')
            if cells[0] == today:
                del(cells[0])
                rows.append(cells)

    for row in rows:
        #if row == rows[0]:
        #    continue
        row[5] = int(row[5])

    # x[5] = count x[2] = trend, x[0] = location, x[8] = nation, x[9] = region
    sorted_rows = sorted(rows, key = lambda x: (x[9], x[8], x[0], x[2], -x[5]))
    return sorted_rows


### WORDPRESS FUNCTIONS ###

def create_wordpress_client(settings_filename):
    config = configparser.ConfigParser()
    config.read(settings_filename)

    url = config.get('wordpress', 'url')
    username = config.get('wordpress', 'user')
    password = config.get('wordpress', 'pass')

    client = Client(url, username, password)

    return client

def generate_post_content_string(report_filename, sort_by):
    content_string = '<table>'
    prev_trend = ""

    with fileinput.input(files=report_filename) as tsv_file:
        if sort_by == 'trend':
            sorted_data = sort_by_trend_count(tsv_file)
        elif sort_by == 'location':
            sorted_data = sort_by_location(tsv_file)

    for cells in sorted_data:
        region = cells[9]
        nation = cells[8]
        location = cells[0]
        trend = cells[2]
        count = cells[5]
        if trend != prev_trend:
            table_row = '<tr><td>' + region + '</td><td>' + nation + '</td><td>' + location + '</td><td>' + trend + '</td><td>' + str(count) + '</td></tr>'
            content_string += table_row
        prev_trend = trend

    content_string += '</table>'
    return content_string

def post_report_to_wordpress(settings_filename, report_filename, sort_by):
    wp = create_wordpress_client(settings_filename)

    filename = report_filename
    content_string = generate_post_content_string(filename, sort_by)
    title = filename[:-4] + '-' + sort_by

    post = WordPressPost()
    post.title = title 
    post.content = content_string

    wp.call(NewPost(post))
    print('%s posted.' % title)


### MAIN ###

def main():
    settings = 'settings.cfg'
    config = configparser.ConfigParser()
    config.read(settings)

    wp = create_wordpress_client(settings)

    draft_posts = wp.call(posts.GetPosts({'post_status': 'draft'}))
    published_posts = wp.call(posts.GetPosts({'post_status': 'published'}))
    print(len(published_posts))

    for post in published_posts:
    	if post.title == "Today's Top Trending Topics (Containing 17) on Twitter":
    		print('replace top 17 post with today\'s data')
    	elif post.title == "Today's Top Trending Topics on Twitter":
    		print('replace top trending post with today\'s data')
    	#print(post.title)


if __name__ == '__main__':
    main()