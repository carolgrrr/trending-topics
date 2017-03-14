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
    #print(wp.call(GetUserInfo()))

    #file upload
    # set to the path to your file
    filename = 'regions-trending-topics-17-2017-03-08.csv'
    content_string = '<table>'

    with open(filename, 'r') as tsv_file:
        for row in tsv_file:
            content_string += '<tr>'
            cells = row.split('\t')
            name = cells[0]
            hashtag = cells[2]
            lat = cells[6]
            lon = cells[7]
            newrow = '<td>' + name + '</td><td>' + hashtag + '</td><td>' + lat + '</td><td>' + lon + '</td>'
            #for cell in cells:
            #    content_string += '<td>'
            #    content_string += cell
            #    content_string += '</td>'
            content_string += newrow 
            content_string += '</tr>'
            #print(cells)

    content_string += '</table>'
    #print(content_string)

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
