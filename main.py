import praw
import os
import pandas as pd
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

reddit = praw.Reddit(
    client_id="KVQGARREpAmG1edIruOYfw",
    client_secret="7YjaJZ2lny3nDZ8x3MkTWjF2UG0NYw",
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.39"
)

subreddit = reddit.subreddit("Bitcoin")
 
# Define the number of posts to retrieve per request
post_limit = 1000

# Define the number of requests to make to retrieve the desired number of posts
num_requests = 1

# Define an empty list to store the post data
post_list = []



# Loop through the requested number of times to retrieve posts
for i in range(num_requests):
    # Get the next batch of posts
    posts = subreddit.new(limit=post_limit, params={'after': '' if i==0 else post_id})
    
    # Keep track of the ID of the last post in the current batch
    post_id = ''
    
    # Loop through each post and extract the relevant information
    for post in posts:
        post_data = {
            'title': post.title.replace("’","'"),
            'author': post.author,
            'url': post.url,
            'permalink': 'https://www.reddit.com' + post.permalink,
            'body': post.selftext.replace("’","'"),
            'score': post.score,
            'created_utc': post.created_utc,
            'num_comments': post.num_comments
        }
        post_list.append(post_data)
        post_id = post.id
    
    # Print the current number of posts retrieved
    print(f"Retrieved {len(post_list)} posts...")
    
    # If we have retrieved the desired number of posts, break out of the loop
    if len(post_list) >= post_limit*num_requests:
        break

# Convert the post data into a Pandas DataFrame
df = pd.DataFrame(post_list)
df.to_csv('bitcoin_posts_new1000.csv', index=False)














# # Get the top 100 posts from the Bitcoin subreddit
# posts = reddit.subreddit('Bitcoin').new(limit=1000)

# # Initialize an empty list to store the post data
# post_list = []

# # Loop through each post and extract the relevant information
# for post in posts:
#     post_data = {
#         'title': post.title.replace("’","'"),
#         'author': post.author,
#         'url': post.url,
#         'body': post.selftext.replace("’","'"),
#         'score': post.score,
#         'created_utc': post.created_utc,
#         'num_comments': post.num_comments
#     }
#     post_list.append(post_data)

# # Convert the post data into a Pandas DataFrame
# df = pd.DataFrame(post_list)
# df.to_csv('bitcoin_posts.csv', index=False)
# # Print the first 5 rows of the DataFrame
# print(df.head())