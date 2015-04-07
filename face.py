import facebook
import requests
from apiclient import errors


# Documents IDs, title, date of creation, creators
posts_IDs = []
post_message = []
_created = []


def extract_posts(graph):
    try:
        # Get the user profile
        profile = graph.get_object('me')
        # Get the user posts
        posts = graph.get_connections(profile['id'], 'posts')

        # Call function with page token
        while 'next' in posts['paging']:
            # Append data of each event to the correspondent array
            if posts != None:
                if 'data' in posts:
                    for post in posts['data']:
                        # Post ID
                        posts_IDs.append(post['id'])
                        # Post message
                        #post_message.append(post['message'].encode('utf8'))
                        print post['message']
                        # Creation date
                        _created.append(post['created_time'][:10] + ' ' + post['created_time'][11:-8])


            posts = requests.get(posts['paging']['next']).json()

        else:
            print "Bad request to Facebook Graph API service or there's no posts in your Facebook."
            return

        return posts_IDs, post_message, _created

    except errors.HttpError, error:
        print 'An error occurred: %s' % error