from typing import List, Union
from datetime import date


LANGUAGE_CODES: List[str] = [
    'en', 'pt', 'ja', 'ber', 'fr', 'es', 'nl', 'de', 'tlh', 'la', 'fi', 'rn', 
    'it', 'id', 'ro', 'hu', 'ga', 'af', 'pl', 'cs', 'tl', 'eo', 'lt', 'is', 
    'et', 'sv', 'da', 'no', 'tr', 'sk', 'lv', 'tk', 'sr', 'vo', 'zh', 'ko', 
    'hi', 'el', 'ru', 'ar'
]

LABELS_CODES: List[str] = [
    'porn', 'sexual', 'nudity', '!no-unauthenticated', 'graphic-media', 
    '!warn', 'spoiler', 'gore', 'nsfw', 'graysky.app', 'circle', 
    'Nudity', '!hide', 'Nsfw', 'nsfl', 'graphic'
]

COLLECTION_CODES: List[str] = [
    'app.bsky.feed.threadgate', 'app.bsky.graph.follow', 'app.bsky.labeler.service', 
    'com.whtwnd.blog.entry', 'app.bsky.graph.block', 'app.bsky.graph.listitem', 
    'app.bsky.feed.repost', 'app.bsky.feed.like', 'app.bsky.actor.profile', 
    'app.bsky.feed.generator', 'app.bsky.feed.post', 'app.bsky.graph.listblock', 
    'app.bsky.feed.postgate', 'app.bsky.graph.list', 'app.bsky.list', 
    'app.bsky.graph.starterpack'
]

PURPOSE_CODES: List[str] = [
    'app.bsky.graph.defs#curatelist',
    'app.bsky.graph.defs#referencelist',
    'app.bsky.graph.defs#modlist',
]

EVENT_CODES: List[str] = [
    'likeAB', 'likeBA', 'followAB', 'followBA', 'repostAB', 'repostBA', 'list_blockAB', 'list_blockBA', 'blockAB', 'blockBA', 
    'listA', 'listB', 'profileA', 'profileB', 
    'postABroot', 'postABparent', 'postBAroot', 'postBAparent',
    'list_itemAB', 'list_itemABcreator', 'list_itemBA', 'list_itemBAcreator'
]



def one_hot_encode_language(lang_code: List[str]) -> Union[List[int], None]:

    one_hot_vector = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    if not lang_code:
        return one_hot_vector

    code_to_index = {code: i for i, code in enumerate(LANGUAGE_CODES)}

    vector_length = len(LANGUAGE_CODES) + 1

    for language in lang_code:
        if language not in LANGUAGE_CODES:
            one_hot_vector[-1] = 1
        else:
            one_index = code_to_index[language]
            one_hot_vector[one_index] = 1

    return one_hot_vector




def one_hot_encode_label(label_code: List[str]) -> Union[List[int], None]:

    one_hot_vector = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    if not label_code:
        return one_hot_vector

    code_to_index = {code: i for i, code in enumerate(LABELS_CODES)}

    vector_length = len(LABELS_CODES) + 1

    for label in label_code:
        if label not in LABELS_CODES:
            one_hot_vector[-1] = 1
        else:
            one_index = code_to_index[label]
            one_hot_vector[one_index] = 1
    
    return one_hot_vector



def one_hot_encode_collection(collection_code: str) -> Union[List[int], None]:
    
    code_to_index = {code: i for i, code in enumerate(COLLECTION_CODES)}
    
    if collection_code not in code_to_index:
        if collection_code != None:
            return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        else:
            return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


    vector_length = len(COLLECTION_CODES)
    
    one_index = code_to_index[collection_code]
    
    
    one_hot_vector = [1 if i == one_index else 0 for i in range(vector_length+1)]
    
    return one_hot_vector




def one_hot_encode_purpose(purpose_code: str) -> Union[List[int], None]:
    
    code_to_index = {code: i for i, code in enumerate(PURPOSE_CODES)}
    
    if purpose_code not in code_to_index:
        if purpose_code != None:
            return [0, 0, 0, 1]
        else:
            return [0, 0, 0, 0]

    vector_length = len(PURPOSE_CODES)
    
    one_index = code_to_index[purpose_code]
    
    one_hot_vector = [1 if i == one_index else 0 for i in range(vector_length+1)]
    
    return one_hot_vector


def one_hot_encode_event(event_code: str) -> Union[List[int], None]:
    
    code_to_index = {code: i for i, code in enumerate(EVENT_CODES)}
    
    if event_code not in code_to_index:
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    vector_length = len(EVENT_CODES)
    
    one_index = code_to_index[event_code]
    
    one_hot_vector = [1 if i == one_index else 0 for i in range(vector_length)]
    
    return one_hot_vector



def encode_date(date: date, initial_date: date):
    if date < initial_date:
        return 0
        
    time_difference = date - initial_date
    
    days_passed = time_difference.days +1 
    
    return days_passed




# print(date_encoding( date(2024,5,7), date(2024,5,6)))

# print(one_hot_encode_event('likeAB'))

# print(one_hot_encode_purpose('app.bsky.graph.defs#curatelist'))

# print(one_hot_encode_collection('app.bsky.graph.starterpack'))

# print(len(one_hot_encode_label('gore')))

# print(len(one_hot_encode_language('ga')))
