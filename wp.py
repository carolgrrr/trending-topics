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

    with open(filename, 'r') as tsv_file:
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


def main():
    wp = create_wordpress_client('settings.cfg')

    filename = 'regions-trending-topics-17-2017-03-08.csv'
    content_string = generate_post_content_string(filename)

    post = WordPressPost()
    post.title = 'Trending Topics Mini Table'
    #post.content = '<table><tr><td>ROW1 COL1 CONTENT</td><td>ROW1 COL2 CONTENT</td><td>ROW1 COL3 CONTENT</td></tr><tr><td>ROW2 COL1 CONTENT</td><td>ROW2 COL2 CONTENT</td><td>ROW2 COL3 CONTENT</td></tr><tr><td>ROW3 COL1 CONTENT</td><td>ROW3 COL2 CONTENT</td><td>ROW3 COL3 CONTENT</td></tr></table>'
    post.content = content_string
    post.terms_names = {
      'post_tag': ['test', 'tables'],
      'category': ['Introductions', 'Tests']
    }
    wp.call(NewPost(post))
    print('end.')

if __name__ == '__main__':
	main()
