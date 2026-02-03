import pickle


# CREATE PICKLE FILE WITH JUST [] INSIDE:

def create_empty_file():
    file_path = "datasets/user2user_events.pkl"

    try:
        with open(file_path, 'wb') as f:
             pickle.dump([], f)
        print(f"Successfully initialized {file_path} with an empty list.")

        with open(file_path, 'rb') as f:
             loaded_content = pickle.load(f)
             print(f"Verification: Content type is {type(loaded_content).__name__} and length is {len(loaded_content)}.")

    except Exception as e:
        print(f"An error occurred during file initialization: {e}")





# #READ THE CONTENT OF THE PICKLE FILE:
def read_pickle():
    with open("datasets/user2user_events.pkl", 'rb') as f:
        loaded_content = pickle.load(f)

    print(len(loaded_content))
    print(loaded_content[:1])
    for row in loaded_content:
        event_list = row["events"]
        start_date = row["start_date"]
        blocks_list = row["blocks"]
        print(event_list)
        print(start_date)
        print(blocks_list)
        break
    with open("datasets/training_X.pkl", 'rb') as f:
        loaded_content = pickle.load(f)
    print(loaded_content[:1])

if __name__ == "__main__":
    read_pickle()