from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
import configparser


def main():
    config = configparser.ConfigParser()
    config.read('settings.cfg')

    url = config.get('wordpress', 'url')
    username = config.get('wordpress', 'user')
    password = config.get('wordpress', 'pass')
    #password = 'RHr&v9LbwJnyesdD0m$1IH5i'

    #print('Hello world.')
    wp = Client(url, username, password)
    #wp.call(GetPosts())
    print(wp.call(GetUserInfo()))

    #file upload
    # set to the path to your file
    filename = 'regions-trending-topics-17-2017-03-08.csv'

    # prepare metadata
    data = {
        'name': 'March 8 Trends',
        'type': 'text/csv',  # mimetype
    }

    # read the binary file and let the XMLRPC library encode it into base64
    #with open(filename, 'rb') as csv_file:
    #    data['bits'] = xmlrpc_client.Binary(csv_file.read())

    response = wp.call(media.UploadFile(data))
    print(response)


    post = WordPressPost()
    post.title = 'Testing tables'
    post.content = '<table><tr><td>ROW1 COL1 CONTENT</td><td>ROW1 COL2 CONTENT</td><td>ROW1 COL3 CONTENT</td></tr><tr><td>ROW2 COL1 CONTENT</td><td>ROW2 COL2 CONTENT</td><td>ROW2 COL3 CONTENT</td></tr><tr><td>ROW3 COL1 CONTENT</td><td>ROW3 COL2 CONTENT</td><td>ROW3 COL3 CONTENT</td></tr></table>'
    post.terms_names = {
      'post_tag': ['test', 'tables'],
      'category': ['Introductions', 'Tests']
    }
    wp.call(NewPost(post))
    print('end.')

if __name__ == '__main__':
	main()
