import pickle
from encoding import one_hot_encode_collection, one_hot_encode_event, one_hot_encode_label, one_hot_encode_language, one_hot_encode_purpose, encode_date, sli_encode_date
import random
from datetime import timedelta

# FILE="datasets/sli_user2user_blocking.pkl"
# DATA_X="datasets/sli_encoded_blocking_X.pkl"
# DATA_Y="datasets/sli_encoded_blocking_Y.pkl"

# FILE="datasets/sli_user2user_non_blocking.pkl"
# DATA_X="datasets/sli_encoded_non_blocking_X.pkl"
# DATA_Y="datasets/sli_encoded_non_blocking_Y.pkl"

# FILE="datasets/more_u2u_non_blocking.pkl"
# DATA_X="datasets/encoded_more_u2u_non_blocking_X.pkl"
# DATA_Y="datasets/encoded_more_u2u_non_blocking_Y.pkl"

FILE="luigi/sli_user2user_non_blocking.pkl"
DATA_X="luigi/encoded_user2user_non_blocking_X.pkl"
DATA_Y="luigi/encoded_user2user_non_blocking_Y.pkl"


MIN_LEN=0
INT_LEN=30


def merge_by_created_date(list1, list2):
    return sorted(
                list1+list2, 
                key=lambda x: (x['created_date'] is None, x['created_date'])
                )



def select_subsequence(events, blocks):
    """
    this functions takes as input the events between 2 users and returns a sequence of events of length INT_LEN
    or less, for the sequences that result in a block it takes a sequence of length INT_LEN before the first block
    skipping 0,1 or 2 events, so the sequence can be used to predict if in the next 3 events there will bee a block
    with the sequence, also a date is return that will be used for the encoding of the created_date attribute.
    this is the day after the last event.
    """

    if len(blocks)>0:
        block_outcome=True

        all_events=merge_by_created_date(events, blocks)

        indx=all_events.index(blocks[0])

        rumor=random.randint(0,2)

        top_indx=indx
        if indx > 3:
            top_indx=indx-rumor

        if top_indx<INT_LEN:
            bottom_indx=0
        else:
            bottom_indx=top_indx-INT_LEN
    
    else:
        block_outcome=False

        all_events=events

        if INT_LEN > len(all_events):
            top_indx=len(all_events)
            bottom_indx=0
        else:
            top_indx=random.randint(INT_LEN,len(all_events))
            bottom_indx=top_indx-INT_LEN

    if top_indx>bottom_indx:
        seq=all_events[bottom_indx:top_indx]
        
        try:
            date= seq[-1]["created_date"] + timedelta(days=1)
        except:
            date=None

        return seq, date, block_outcome
    else:
        return [], None, block_outcome




with open(FILE, 'rb') as f:
    dataset = pickle.load(f)



encoded_interactions_X=[]
encoded_interactions_Y=[]

for interaction in dataset:
    event_list=interaction["events"]
    blocks_list=interaction["blocks"]

    seq,reference_date,block_outcome=select_subsequence(event_list,blocks_list)

    encoded_interaction=[]

    for event in seq:
        
        try:
            event_type=event["event"]
        except:
            event_type=None

        try:
            created_date=event["created_date"]
        except:
            created_date=None

        try:
            collection=event["collection"]
        except:
            collection=None

        try:
            label=event["label"]
        except:
            label=None

        try:
            purpose=event["purpose"]
        except:
            purpose=None

        try:
            languages=event["languages"]
        except:
            languages=None

        #encoded_row=one_hot_encode_event(event_type)+[encode_date(created_date, start_date)]+ one_hot_encode_collection(collection)+one_hot_encode_label(label)+one_hot_encode_purpose(purpose)+one_hot_encode_language(languages)
        encoded_event=one_hot_encode_event(event_type)+[sli_encode_date(created_date, reference_date)]+ one_hot_encode_collection(collection)+one_hot_encode_label(label)+one_hot_encode_purpose(purpose)+one_hot_encode_language(languages)

        encoded_interaction.append(encoded_event)
    
    encoded_interactions_X.append(encoded_interaction)

    encoded_interactions_Y.append(1 if block_outcome else 0)


with open(DATA_X, "wb") as f:
    pickle.dump(encoded_interactions_X, f)

with open(DATA_Y, "wb") as f:
    pickle.dump(encoded_interactions_Y, f)


