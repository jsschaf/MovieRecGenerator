def parseUser(u):
    new_u = { key: u[key] for key in [
        'created_at',
        'description',
        'entities',
        'favourites_count',
        'followers_count',
        'friends_count',
        'id',
        'id_str',
        'lang',
        'listed_count',
        'location',
        'name',
        'screen_name',
        'statuses_count',
        'url'
        ]
    }
    return new_u

def parseTweet(s):
    new_s = { key: s[key] for key in [
        'created_at',
        'entities',
        'favorite_count',
        'id',
        'id_str',
        'lang',
        'metadata',
        'text',
        'source'
        ]
    }
    new_s['user'] = parseUser(s['user'])
    return new_s

def parseUserBasic(u):
    new_u = { key: u[key] for key in [
        'description',
        'id',
        'id_str',
        'screen_name'
        ]
    }
    return new_u

def parseTweetBasic(s):
    new_s = { key: s[key] for key in [
        'created_at',
        'id',
        'id_str',
        # 'entities',
        'text'
        ]
    }
    new_s['user'] = parseUserBasic(s['user'])
    return new_s
