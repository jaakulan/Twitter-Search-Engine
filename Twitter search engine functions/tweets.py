from typing import List, Dict, TextIO, Tuple

HASH_SYMBOL = '#'
MENTION_SYMBOL = '@'
URL_START = 'http'

# Order of data in the file                                                      
FILE_DATE_INDEX = 0
FILE_LOCATION_INDEX = 1
FILE_SOURCE_INDEX = 2
FILE_FAVOURITE_INDEX = 3
FILE_RETWEET_INDEX = 4

# Order of data in a tweet tuple
TWEET_TEXT_INDEX = 0
TWEET_DATE_INDEX = 1
TWEET_SOURCE_INDEX = 2
TWEET_FAVOURITE_INDEX = 3
TWEET_RETWEET_INDEX = 4

# Helper functions.

def alnum_prefix(text: str) -> str:
    """Return the alphanumeric prefix of text, converted to
    lowercase. That is, return all characters in text from the
    beginning until the first non-alphanumeric character or until the
    end of text, if text does not contain any non-alphanumeric
    characters.

    >>> alnum_prefix('')
    ''
    >>> alnum_prefix('IamIamIam')
    'iamiamiam'
    >>> alnum_prefix('IamIamIam!!')
    'iamiamiam'
    >>> alnum_prefix('IamIamIam!!andMore')
    'iamiamiam'
    >>> alnum_prefix('$$$money')
    ''

    """

    index = 0
    while index < len(text) and text[index].isalnum():
        index += 1
    return text[:index].lower()


def clean_word(word: str) -> str:
    """Return all alphanumeric characters from word, in the same order as
    they appear in word, converted to lowercase.

    >>> clean_word('')
    ''
    >>> clean_word('AlreadyClean?')
    'alreadyclean'
    >>> clean_word('very123mes$_sy?')
    'very123messy'

    """

    cleaned_word = ''
    for char in word.lower():
        if char.isalnum():
            cleaned_word = cleaned_word + char
    return cleaned_word


# Required functions

def extract_mentions(text: str) -> List[str]:
    """Return a list of all mentions in text, converted to lowercase, with
    duplicates included.

    >>> extract_mentions('Hi @UofT do you like @cats @CAT!S #meowmeow')
    ['uoft', 'cats', 'cats']
    >>> extract_mentions('@cats are #cute @cats @cat meow @meow')
    ['cats', 'cats', 'cat', 'meow']
    >>> extract_mentions('@many @cats$extra @meow?!')
    ['many', 'cats', 'meow']
    >>> extract_mentions('No valid mentions @! here?')
    []

    """
    extracted = []
    split_text = text.split(" ")
    
    while '' in split_text:
        split_text.remove('')      
    
    for words in split_text:
        if words[0] == MENTION_SYMBOL:
            if not alnum_prefix(words[1:]) == '': 
                extracted.append(alnum_prefix(words[1:]))
                
    return extracted

def extract_hashtags(text: str) -> List[str]:
    """Return a list of all hashtags in text, converted to lowercase, with
    duplicates discluded.

    >>> extract_hashtags('Hi #UofT do you like #cats #CAT!S #meowmeow')
    ['uoft', 'cats',]
    >>> extract_hashtags('#cats are #cute #cats #cat meow #meow')
    ['cats', 'cat', 'meow']
    >>> extract_hashtags('#many #cats$extra #meow?!')
    ['many', 'cats', 'meow']
    >>> extract_hashtags('No valid mentions #! #! #! here?')
    []
    >>> extract_hashtags('Congratulations to all our fall graduates!  https://t.co/iRXYwYUAKa\n)
    []

    """
    extracted = []
    unique_extracted = []
    split_text = text.split(" ")
    
    while '' in split_text:
        split_text.remove('')    
    
    for words in split_text:
        if words[0] == HASH_SYMBOL:
            if not alnum_prefix(words[1:]) == '': 
                extracted.append(alnum_prefix(words[1:]))
                
    for hashtags in extracted: 
        if hashtags not in unique_extracted: 
            unique_extracted.append(hashtags) 
    
    return unique_extracted

def count_words(text: str, dict_words: dict) -> None:
    """
    update the given dictionary with the frequency of the words seen in the text
    
    >>>count_words('Hi #UofT do you like #cats #CAT!S #meowmeow', \
                   {'hi': 1, 'you': 2})
    {'hi': 2, 'you': 3, 'do': 1, 'like': 1}
    >>>count_words('Today! @nickfrosst is a panelist at #StartAI!\
                #uoftalumni #UofT https://t.co/k50ea9qKhb (via @UofTNews)', {})
    {'today': 1, 'is': 1, 'a': 1, 'panelist': 1, 'at': 1, 'via': 1}           
    """
    t_words = []
    for word in text.split():
        if not (word[0] == MENTION_SYMBOL or word[0] == HASH_SYMBOL or\
                URL_START in word):
            t_words.append(clean_word(word))
    
    for word in t_words:
        if word in dict_words:
            dict_words[word] = dict_words[word] + 1
        else:
            dict_words[word] = 1

def common_words(dict_words: dict, limit: int) -> None:
    """
    find the N most appearing words, if there is tie that breaks the limit, it
    doesn't include all the words witht he same number breaking the limit
    
    common_words({'like': 9, 'hi': 7, 'do': 7, 'you': 3, 'kol':4,\
                 'bol':5, 'jol':5}, 2)
    {'like': 9}
    common_words({'a': 3, 'b': 3}, 1)
    {}
    """
    new_dict_words = {}
    listofkeys = []
    #sort the values of the keys in the dict_words into a list
    dict_word_num = sorted(dict_words.values())
    dict_word_num[::-1] = dict_word_num
    
    #puts the values of the N most frequent words into a list
    if not len(dict_words) <= limit:
        common = limit_frequent_values(dict_word_num, limit) 
        dict_words_list = dict_words.items()
     
     #makes a new dictionary using the values from common to find the N most
     #frequent dictionary words
        for num in common:
            for words in dict_words_list:
                if words[1] == num:
                    listofkeys.append(words[0])
                    
        for key_words in listofkeys:
            new_dict_words[key_words] = dict_words[key_words]  

        dict_words.clear()  
        dict_words.update(new_dict_words)
    
def limit_frequent_values(dict_word_num: list, limit: int) -> list:
    """finds values in a list and only keep N amount of the left of the list
    
    >>>limit_frequent_values([3, 2, 1], 3)
    [3, 2, 1]
    >>>limit_frequent_values([3, 2, 1], 4)
    [3, 2, 1]
    >>>limit_frequent_values([3, 2, 1], 0)
    []
    """
    x = 0
    common = []
    #finds the N most numbers in the list, by counting the amount of times a
    #number appears, and seeing if the number could be placed into the list 
    #without going past the N limit
    y = len(dict_word_num)
    while y > 0:
        if dict_word_num.count(max(dict_word_num[x:])) <= limit - x:
            common.append(max(dict_word_num[x:]))
            x = x + dict_word_num.count(max(dict_word_num[x:]))
        else:
            break
        y = y - 1
    
    return common
    
def read_tweets(tweet_data: TextIO) ->  Dict[str, List[tuple]]:
    """
    creates a dictionary for users that display all their tweet and
    information in a tuple of 
    (tweet text, date, source, favourite count, retweet count)
    
    >>>read_tweets(open("C:\\Users\\Jaakulan S\\Desktop\\a3\\tweets_small.txt"))
    {'uoftcompsci': [('RT @_AlecJacobson: @UofTCompSci St. George\
    (Downtown) Campus is hiring in Computational Geometry for a\
    Tenure Stream Faculty Position.\
    Tell your friends!\n\nhttps://t.co/O9Oui82dEA\n', '20181108132750',\
    'Unknown Location', '0', '5'), ('Congratulations to all our fall graduates!\
    https://t.co/iRXYwYUAKa\n', '20181106202405', 'Toronto Ontario', '6', '1'),\
    ("RT @UaigUoft: And... it's a wrap!\n\nThank you to all our speakers,\
    sponsors, and attendees for making\
    #StartAI an unforgettable experience for us.\
    We hope you feel the same. \n\nTweet us your StartAI photos!\
    https://t.co/5zi4AAAyfS\n", '20181104014855', 'Unknown Location', '0',\
    '2'), ('Today! @nickfrosst is a panelist at#StartAI!\
    #uoftalumni #UofT https://t.co/k50ea9qKhb (via @UofTNews)\n',\
    '20181103122515', 'Toronto Ontario', '5', '0')]}
    """
    lines_twitter_text = tweet_data.readlines()
    tweets_dict = {}  
    clean_twitter_text = twitter_text_cleaner(lines_twitter_text)
    eot_list = eot_lister(clean_twitter_text)
    
    #beginning at the tweet start indicated by an EOT index, if the word after
    #is a user name the first if statement will format it into the dictionary 
    #and find the tweets until the end of the user's tweets 
    for i in eot_list:
        if len(clean_twitter_text[i+1].split(',')) == 1:
            format_user_tweets(clean_twitter_text, eot_list, tweets_dict, i)
            x = clean_twitter_text[i+1][:-2]
        else:
            format_other_tweets(clean_twitter_text, eot_list, tweets_dict, i, x)            
    
    #message = "uoft" if 'uoft' in tweets_dict else "booh"
    #print(message)            
    return tweets_dict

def format_user_tweets(clean_twitter_text: list, eot_list: list,\
                       tweets_dict: dict, i: int) -> None:
    """Format user's tweets into a dictionary along with the tweets info
    
    >>>format_user_tweets(clean_twitter_text, eot_list, tweets_dict, i)
    """
    #uses the splti function to find out if there is a new username with tweets
    #to be inputed, if not tweets continue to be input into the original user
    if len(clean_twitter_text[i + 2].split(",")) == 5:
        a, b, c, d, e = clean_twitter_text[i + 2].split(",")
        k = c
        e = e[:-1]
        tweets_dict[clean_twitter_text[i + 1][:-2].lower()] = []
    else:
        tweets_dict[clean_twitter_text[i + 1][:-2].lower()] = []
        a, b, c, d, e = clean_twitter_text[i + 3].split(",")
        k = c
        e = e[:-1]
        tweets_dict[clean_twitter_text[i + 2][:-2].lower()] = []                             
    #uses EOT indexes to carefully input the last tweet along with any
    #information from the user
    if eot_list[eot_list.index(i)] == eot_list[-1]:
        b = clean_twitter_text[i + 3:]
    else:
        b = clean_twitter_text[i + 3: eot_list[eot_list.index(i)+1]]              
    b = tweet_fixer(b)        
    tweet_info = (b, a, k, d, e)
    tweets_dict[clean_twitter_text[i + 1][:-2].lower()].append(tweet_info)

def format_other_tweets(clean_twitter_text: list, eot_list: list,\
                        tweets_dict: dict, i: int, x: str) -> None:
    """Formats user's last tweets into a dictionary along with tweet info
    
    >>>format_other_tweets(clean_twitter_text, eot_list, tweets_dict, i, x)
    """
    #use the split to find if there are users and when there isn't these tweets
    #go to the last user in the dictionary
    a, b, c, d, e = clean_twitter_text[i + 1].split(",")
    k = c
    e = e[:-1]
    if eot_list[eot_list.index(i)] == eot_list[-1]:
        b = clean_twitter_text[i + 2:]
    else:
        b = clean_twitter_text[i + 2: eot_list[eot_list.index(i)+1]]  
    b = tweet_fixer(b)
    tweet_info = (b, a, k, d, e)
    tweets_dict[x.lower()].append(tweet_info)     

def eot_lister(clean_twitter_text: list) -> list:
    """ return the indexes of all '>>>EOT\n' in the str split into a 
    list of words from tweet data
    
    >>>eot_lister(clean_twitter_text_small)
    [0, 6, 9, 16]
    """
    eot_list = []
    eot_holder = 0
    
    for lines in clean_twitter_text:
        if lines == '<<<EOT\n':
            eot_list.append(eot_holder)
            eot_holder = eot_holder + 1
        else:
            eot_holder = eot_holder + 1
    return eot_list

def twitter_text_cleaner(tweet_list: list) -> list:
    """Return a list of tweets, from a formated tweet text document cleaned into
    a format to recieve info from
    
    >>>twitter_text_cleaner(['UofTCompSci:', '20181108132750',\
                         'Unknown Location', 'Twitter for Android', '0','5',\
                         '<<<EOT\n'])
    ['<<<EOT\n', 'UofTCompSci:', '20181108132750',\
                         'Unknown Location', 'Twitter for Android', '0','5',]
    """
    while '' in tweet_list:
        tweet_list.remove('')
    
    tweet_list.pop(-1)
    tweet_list.insert(0, '<<<EOT\n')
    
    return tweet_list

def tweet_fixer(b: list) -> str:
    """returns a string tweet fixed with no whitespace
    >>>tweet_fixer([   'c', 'a', 'b'   ])
    'cab'
    """
    b = ''.join(b)
    b.lstrip()
    b.rstrip()
    return b
    
    
def most_popular(tweet_info: dict, date1: int, date2: int) -> str:
    """Return the user of the most popular tweet between two dates
    
    >>>most_popular\
    (read_tweets(open("C:\\Users\\Jaakulan S\\Desktop\\a3\\tweets_big.txt")),\
    20181109190529, 20181103161630)
    'uoftcompsci'
    >>>most_popular({'uoftcompsci':[], 'uoft':[]}, 20181109190529, 20181103161630)
    'tie'
    """
    popular_tweets = popular_tweets_dict(tweet_info, date2, date1)
    most_popular_tweet = {}
    
    #if there all users dont have tweets in the dictionary, it will
    #result in a tie
    for key in popular_tweets:
        end_function = 0
        if popular_tweets[key] != []:
            end_function = end_function + 1
    
    if end_function == 0:
        return "tie"
    
    for key in popular_tweets:
        if len(popular_tweets[key]) >= 1:
            most_popular_tweet[key] = max(popular_tweets[key])
            
    most_popular_user\
        = find_popular_user(popular_tweets, most_popular_tweet)
    
    return most_popular_user
    
def popular_tweets_dict(tweet_info: dict, date2: int, date1: int) -> dict:
    """return a dictionary of tweets between two dates
    
    >>>popular_tweets_dict\
    (read_tweets(open("C:\\Users\\Jaakulan S\\Desktop\\a3\\tweets_big.txt")),\
    20181103161630, 20181109190529)
    {'uoftcompsci': [27, 7, 5, 3, 1, 0, 4, 19, 2, 4, 4, 2, 3, 62, 2, 2, 4],\
    'uoftartsci': [0, 1, 25], 'uoft': [], 'utsc': [],\
    'utm': [8, 5, 0, 7, 1], 'uoftnews': [15, 2]}
    """
    
    popular_tweets = {}
    
    for key in tweet_info:
        popular_tweets[key] = []
        for value in tweet_info[key]:
            x = 0          
            if date2 <= int(value[1]) <= date1: 
                for counts in value[4:]:
                    x = int(counts) + x
                popular_tweets[key].append(x)
                
    return popular_tweets

def find_popular_user(popular_tweets: list, most_popular_tweet: dict) -> str:
    """return the most popular user or a tie between the users if there are more
    than one
    
    >>>find_popular_user(popular_tweets_dict\
    (read_tweets(open("C:\\Users\\Jaakulan S\\Desktop\\a3\\tweets_big.txt")),\
    20181103161630, 20181109190529),\
    {'uoftcompsci': 62, 'uoftartsci': 25, 'utm': 8, 'uoftnews': 15})
    'uoftcompsci'
    """
    users = []
        
    for key in popular_tweets:
        if len(popular_tweets[key]) >= 1:
            most_popular_tweet[key] = max(popular_tweets[key])
            
    popularity = most_popular_tweet[(max(most_popular_tweet,\
                                         key=most_popular_tweet.get))]
    
    for key in most_popular_tweet:
        if most_popular_tweet[key] == popularity:
            users.append(key)
    
    if len(users) == 1:
        return users[0]
    else:
        return 'tie'    
           
def detect_author(tweet_info: dict, unknown_tweet: str) -> str:
    """
    return the most-likely author of the unknown tweet, only found if all the 
    hashtags in the tweet match all the hashtags the author's uses
    
    >>>detect_author(read_tweets(open\
    ("C:\\Users\\Jaakulan S\\Desktop\\a3\\tweets_big.txt")), '#uoft')
    'unknown'
    >>>detect_author(read_tweets(open\
    ("C:\\Users\\Jaakulan S\\Desktop\\a3\\tweets_big.txt")),\
    '#uoft #STARTAI #UOFTALUMNI!')
    'uoftcompsci'
    >>>detect_author(read_tweets(open\
    ("C:\\Users\\Jaakulan S\\Desktop\\a3\\tweets_big.txt")), '#utsc #utsc')
    'unknown'
    """
    tweet_authors = {}
    #put all the hashtags that the users ever used into a list without it
    #repeating and sort it alphabetically. Afterward the hashtags are put into
    #their respective user keys as a list
    for key in tweet_info:
        tweet_authors[key] = []
        for value in tweet_info[key]:
            tweet_authors_list = []
            for hashtags in extract_hashtags(value[0]):
                tweet_authors_list.append(hashtags)
                unique_tweet_authors_list = []                
            for words in tweet_authors_list: 
                if words not in unique_tweet_authors_list:
                    unique_tweet_authors_list.append(words)
            unique_tweet_authors_list.sort()
        tweet_authors[key] = unique_tweet_authors_list
    
    #uses the helper function to find the most likely user
    return (suspect_author(tweet_authors, unknown_tweet))
    
def suspect_author(tweet_authors: dict, unknown_tweet: str) -> str:
    """return the author who used the same hashtags as the unknown tweet
    
    >>>suspect_author(read_tweets(open(\
    "C:\\Users\\Jaakulan S\\Desktop\\a3\\tweets_big.txt")), '#uoft')
    'unknown'
    """
    author_hashtags = extract_hashtags(unknown_tweet)
    author_hashtags.sort()
    suspected_authors = []
    
    #find the most likely users of a tweet
    for keys in tweet_authors:
        if tweet_authors[keys] == author_hashtags:
            suspected_authors.append(keys)
  
    if len(suspected_authors) == 1:
        return suspected_authors[0]
    else:
        return 'unknown'    

#if __name__ == '__main__':

    #pass

    # If you add any function calls for testing, put them here.
    # Make sure they are indented, so they are within the if statement body.
    # That includes all calls on print, open, and doctest.

    # import doctest
    # doctest.testmod()
