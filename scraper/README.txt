This program scrapes the data from FIREHOSE using a single thread,
it saves the type of action (example "app.bsky.feed.like") in the "actions.json", and it filters the type of data based on those actions
and saves the data in a jsonl file.

libraries to download:
-atproto

CONFIG FILE:
    "firehose": {
        "output_file": "30-10-25.jsonl", -> name of the outputfile
        "verbose": true -> to print the various phases of data
    },
    "scraping": {
        "time_limit": 10, -> seconds of scraping
        "action_limit": 100000 -> number of post before ending the scraping
    },
    "actions": {
        "filename" : "actions.json",
        "save": true -> do I save new "actions"?
    }


Right now we can only scrape the post data
TODO:
expand the type of action to scrape
    ->add method _extract_typeOfAction_data
        ->do it in the way you want
    ->add the corrisponding key-value in the ACTION HANDLER dictionary in the _process_CAR_data method