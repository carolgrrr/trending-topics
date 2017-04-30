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


def main():
    settings = 'settings.cfg'
    config = configparser.ConfigParser()
    config.read(settings)

    wp = create_wordpress_client(settings)

    draft_posts = wp.call(posts.GetPosts({'post_status': 'draft'}))
    published_posts = wp.call(posts.GetPosts({'post_status': 'published'}))
    print(len(published_posts))

    for post in draft_posts:
    	print(post.title)



if __name__ == '__main__':
    main()