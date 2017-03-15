from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
import configparser

def create_wordpress_client(settings_filename):
    config = configparser.ConfigParser()
    config.read(settings_filename)

    url = config.get('wordpress', 'url')
    username = config.get('wordpress', 'user')
    password = config.get('wordpress', 'pass')

    client = Client(url, username, password)

    return client

def generate_post_content_string(report_filename):
    content_string = '<table>'

    with open(report_filename, 'r') as tsv_file:
        for row in tsv_file:
            cells = row.split('\t')
            region = cells[9]
            nation = cells[8]
            location = cells[0]
            trend = cells[2]
            count = cells[5]
            table_row = '<tr><td>' + region + '</td><td>' + nation + '</td><td>' + location + '</td><td>' + trend + '</td><td>' + count + '</td></tr>'
            content_string += table_row

    content_string += '</table>'
    return content_string

def post_report_to_wordpress(settings_filename, report_filename):
    wp = create_wordpress_client(settings_filename)

    filename = report_filename
    content_string = generate_post_content_string(filename)
    title = filename[:-4]

    post = WordPressPost()
    post.title = title
    post.content = content_string

    wp.call(NewPost(post))
    print('posted.')


def main():
    settings = 'settings.cfg'
    report = 'regions-trending-topics-17-2017-03-08.csv'
    post_report_to_wordpress(settings, report)

if __name__ == '__main__':
	main()
