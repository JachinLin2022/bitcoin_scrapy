import requests

import json
import time

import pandas as pd

url = 'https://twitter.com/i/api/2/search/adaptive.json'
output = './tweet/test.csv'
proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}
params = {
    'include_profile_interstitial_type': '1',
    'include_blocking': '1',
    'include_blocked_by': '1',
    'include_followed_by': '1',
    'include_want_retweets': '1',
    'include_mute_edge': '1',
    'include_can_dm': '1',
    'include_can_media_tag': '1',
    'include_ext_has_nft_avatar': '1',
    'include_ext_is_blue_verified': '1',
    'include_ext_verified_type': '1',
    'include_ext_profile_image_shape': '1',
    'skip_status': '1',
    'cards_platform': 'Web-12',
    'include_cards': '1',
    'include_ext_alt_text': 'true',
    'include_ext_limited_action_results': 'false',
    'include_quote_count': 'true',
    'include_reply_count': '1',
    'tweet_mode': 'extended',
    'include_ext_views': 'true',
    'include_entities': 'true',
    'include_user_entities': 'true',
    'include_ext_media_color':'true',
    'include_ext_media_availability':'true',
    'include_ext_sensitive_media_warning':'true',
    'include_ext_trusted_friends_metadata':'true',
    'send_error_codes':'true',
    'simple_quoted_tweet':'true',
    'tweet_search_mode':'live',
    'q': '#bitcoin lang:en',
    'cursor': 'scroll:thGAVUV0VFVBaAwLOBlOzg5C0WgoCwifKl--QtEnEVnOl2FYCJehgHREVGQVVMVDUBFfQDFQAA',
    'vertical': 'default',
    'query_source': 'typed_query',
    'count': '20',
    'requestContext': 'launch',
    'pc': '1',
    'spelling_corrections': '1',
    'include_ext_edit_control':'true',
    'ext': 'mediaStats,highlightedLabel,hasNftAvatar,voiceInfo,birdwatchPivot,enrichments,superFollowMetadata,unmentionInfo,editControl,vibe'
}


header = {
    'Host': 'twitter.com',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48',
    'Accept-Encoding': 'gzip, deflate, br'
}

with open('header.txt', 'r') as file:
    for line in file:
        if line.startswith('cookie') or line.startswith('authorization') or line.startswith('x-csrf-token'):
            key, value = line.strip().split(": ")
            header[key] = value

print(header)
# urls = 'https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&include_ext_is_blue_verified=1&include_ext_verified_type=1&include_ext_profile_image_shape=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_ext_limited_action_results=false&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_ext_views=true&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&q=%23bitcoin&vertical=default&query_source=typd&count=20&requestContext=launch&pc=1&spelling_corrections=1&include_ext_edit_control=true&ext=mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CvoiceInfo%2CbirdwatchPivot%2Cenrichments%2CsuperFollowMetadata%2CunmentionInfo%2CeditControl%2Cvibe'


def fetch_url(url, params, header, num_retries=10):
    try:
        response = requests.get(url=url,params=params,headers=header,proxies=proxies,verify=False)
    except:
        if num_retries > 0:
            time.sleep(1)
            print('retry')
            return fetch_url(url, params, header, num_retries-1)
        else:
            raise Exception('Failed to fetch url')
    if response.status_code != 200:
        print(response.content)
        if num_retries > 0:
            time.sleep(1)
            print('retry2')
            return fetch_url(url, params, header, num_retries-1)
        else:
            raise Exception('Failed to fetch url')
    return response



res = []
for i in range(1):
    # r = requests.get(url=url,params=params,headers=header,verify=False)
    r = fetch_url(url, params, header)
    print(r.status_code)
    msg = json.loads(r.content)
    tweets = msg['globalObjects']['tweets']
    
    

    
    # print(len(msg['timeline']['instructions']) )
    
    for ins in msg['timeline']['instructions']:
        if 'addEntries' in ins:
            cursors = ins['addEntries']['entries']
            for cursor in cursors:
                if cursor['entryId'].find('cursor-bottom') >= 0:
                    # print(cursor['content']['operation']['cursor']['value'])
                    params['cursor'] = cursor['content']['operation']['cursor']['value']
        else:
            cursors = ins['replaceEntry']['entry']
            if cursors['entryId'].find('cursor-bottom') >= 0:
                params['cursor'] = cursors['content']['operation']['cursor']['value']
    
    # if len(msg['timeline']['instructions']) == 1:
    #     cursors = msg['timeline']['instructions'][0]['addEntries']['entries']
    #     for cursor in cursors:
    #         if cursor['entryId'].find('cursor-bottom') >= 0:
    #             # print(cursor['content']['operation']['cursor']['value'])
    #             params['cursor'] = cursor['content']['operation']['cursor']['value']
    # else:
    #     # print(msg['timeline']['instructions'][2].keys())
    #     cursors = msg['timeline']['instructions'][2]['replaceEntry']['entry']
    #     params['cursor'] = cursors['content']['operation']['cursor']['value']



    for tweet_time_line in tweets.keys():
        tweet = tweets[tweet_time_line]
        scrapy_tweet = {
            'id': tweet_time_line,
            'full_text': tweet['full_text'],
            'created_at': tweet['created_at'],
            'favorite_count': tweet['favorite_count'],
            'quote_count':tweet['quote_count'],
            'reply_count':tweet['reply_count'],
            'retweet_count':tweet['retweet_count'],
            'cursor': params['cursor']
        }
        res.append(scrapy_tweet)


    if i > 0 and i % 10 ==0 :
        df = pd.DataFrame(res, columns=['id','full_text', 'created_at', 'favorite_count','quote_count', 'reply_count', 'retweet_count', 'cursor'])
        df.to_csv(output,index=False)
        print(df)

df = pd.DataFrame(res, columns=['id','full_text', 'created_at', 'favorite_count','quote_count', 'reply_count', 'retweet_count'])
df.to_csv(output,index=False)
print(df)


