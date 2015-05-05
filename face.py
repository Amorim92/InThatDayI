import facebook
import requests
from apiclient import errors


# Posts IDs, posts messages, creation dates
posts_IDs = []
posts_message = []
status_types = []
likes = []
creators = []
_created = []


def extract_posts(service, token, before, after):
    try:
        # Get the user profile
        profile = service.get_object('me')
        # Get the user posts
        posts = service.get_connections(profile['id'], 'posts')

        # Call function with page token
       
        # Append data of each event to the correspondent array
        if posts != None:
            if 'data' in posts:
                for post in posts['data']:
                    # Post ID
                    posts_IDs.append(post['id'])
                    # Post message
                    # posts_message.append(post['message'].encode('utf8'))
                    # Status type of the post
                    status_types.append(post['status_type'])
                    # Creator
                    creators.append(post['from']['name'])
                    # Creation date
                    _created.append(post['created_time'][:16].replace('T', ' '))
                    
                    # People who liked the post
                    if 'likes' in post:
                        for person in post['likes']['data']:
                            likes.append(person['name'])

            # posts = requests.get(posts['paging']['next']).json()
        else:
            print "Bad request to Facebook Graph API service or there's no posts in your Facebook."
            return

        print posts_IDs, likes
        # return posts_IDs, post_message, _created

    except errors.HttpError, error:
        print 'An error occurred during post extraction: %s' % error