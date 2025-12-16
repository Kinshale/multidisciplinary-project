import pickle
from encoding import one_hot_encode_collection, one_hot_encode_event, one_hot_encode_label, one_hot_encode_language, one_hot_encode_purpose, encode_date

FILE="datasets/user2user_events.pkl"
DATA_X="datasets/training_X.pkl"
DATA_Y="datasets/training_Y.pkl"

with open(FILE, 'rb') as f:
    dataset = pickle.load(f)


training_set_X=[]
training_set_Y=[]

for row in dataset:
    event_list=row["events"]
    start_date=row["start_date"]
    blocks_list=row["blocks"]


    encoded_rows=[]

    for event in event_list:
        
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

        encoded_row=one_hot_encode_event(event_type)+[encode_date(created_date, start_date)]+ one_hot_encode_collection(collection)+one_hot_encode_label(label)+one_hot_encode_purpose(purpose)+one_hot_encode_language(languages)
        encoded_rows.append(encoded_row)
    
    training_set_X.append(encoded_rows)


    blockAB=0
    blockBA=0

    for block in blocks_list:
        if block["event"]=="blockAB":
            blockAB=1
        elif block["event"]=="blockBA":
            blockBA=1
        else:
            pass

    training_set_Y.append([blockAB, blockBA])

with open(DATA_X, "wb") as f:
    pickle.dump(training_set_X, f)

with open(DATA_Y, "wb") as f:
    pickle.dump(training_set_Y, f)
