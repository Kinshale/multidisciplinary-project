from atproto import FirehoseSubscribeReposClient, parse_subscribe_repos_message, CAR, IdResolver, DidInMemoryCache
import json
import time
from datetime import datetime
import threading
import re
import os

def load_json_file(filename):
    """Safely load JSON file with error handling"""
    if not os.path.exists(filename):
        print(f"File {filename} does not exist")
        return []

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            if os.path.getsize(filename) == 0:
                return []
            return json.load(f)

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from {filename}: {e}")
        return []
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return []

def append_to_jsonl(data, filename=None):
    """Append data to JSONL file - automatically continues from previous runs"""
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"data_{timestamp}.json"

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            if isinstance(data, set):
                data = list(data)
            json_line = json.dumps(data, ensure_ascii=False)
            f.write(json_line + '\n')
    except Exception as e:
        print(f"Error appending to JSONL file: {e}")


class Config:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.data = self._load_config()

    def _load_config(self):
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Config file {self.config_file} not found")

        with open(self.config_file, 'r') as f:
            return json.load(f)

    def get(self, key, default=None):
        """Get config value using dot notation: 'database.host'"""
        keys = key.split('.')
        value = self.data
        for k in keys:
            value = value.get(k, {})
        return value if value != {} else default

    def __getitem__(self, key):
        return


class ActionClassifier:
    def __init__(self, filename,action_save):
        self.seen_actions = set(load_json_file(filename))
        self.filename = filename
        self.action_save = action_save
        return


    def add_action(self, action):
        if not self.action_save:
            return
        self.seen_actions.add(action)
        return

    def save_new_actions(self):
        if not self.action_save:
            return
        append_to_jsonl(self.seen_actions, self.filename)


class FirehoseScraper:
    def __init__(self, action_classifier, output_file=None, verbose=False):
        self.action_classifier = action_classifier
        self.output_file = output_file
        self.resolver = IdResolver(cache=DidInMemoryCache())
        self.actionScraper = ActionScraper(action_classifier, verbose)
        self.post_count = 0
        self.running = False
        self.verbose = verbose

    def _firehose_callback(self, message):
        """Callback function for FirehoseSubscribeReposClient"""
        try:
            # Process the message through your ActionScraper
            self.actionScraper.process_action(message, self.resolver, self.output_file)
            self.post_count += 1

        except Exception as e:
            print(f"Error in firehose callback: {e}")

    def start_collection(self, duration_seconds=30, post_limit=None):

        self.start_time = time.time()
        end_time = self.start_time + duration_seconds if duration_seconds else None
        self.running = True

        def check_limits():
            while self.running:
                current_time = time.time()
                print(f"Current time: {current_time}" + f" Time left:  {end_time - current_time}")
                if duration_seconds and current_time >= end_time:
                    print("\nTime limit reached.")
                    self._stop_collection()
                    break
                elif post_limit and self.post_count >= post_limit:
                    print("\nPost limit reached.")
                    self._stop_collection()
                    break
                time.sleep(1)  # Check every second

        try:
            # Start limit checking in a separate thread
            limit_thread = threading.Thread(target=check_limits)
            limit_thread.daemon = True
            limit_thread.start()

            self.client = FirehoseSubscribeReposClient()
            self.client.start(self._firehose_callback)

        except Exception as e:
            print(f"Error in firehose collection: {e}")
            self.running = False

        return

    def _stop_collection(self):

        self.running = False
        elapsed = time.time() - self.start_time
        print(f"\nCollection stopped")
        print(f"Total posts processed: {self.post_count}")
        print(f"Elapsed time: {elapsed:.2f} seconds")

        self.action_classifier.save_new_actions()
        self.client.stop()
        print("\nCollection stopped")
        return

def classify_type_action(path, action_classifier):
    # Match the pattern: namespace.action/record_id
    match = re.match(r'([a-z]+\.[a-z]+\.[a-z]+)\.([a-z]+)/(.+)', path)
    if not match:
        return
    namespace = match.group(1)  # "app.bsky.feed"
    action = match.group(2)  # "like"
    record_id = match.group(3)  # "3lcaqus3rxq2c"

    # print(f"Namespace: {namespace}" + f" Action: {action}" + f" RecordID: {record_id}")

    action_classifier.add_action(namespace + '.' +action)
    return namespace + '.' +action

class ActionScraper:
    def __init__(self,action_classifier, verbose=False):
        self.action_classifier = action_classifier
        self.verbose = verbose

    def process_action(self,message, resolver, output_file):
        try:
            commit = parse_subscribe_repos_message(message)

            if self.verbose:
                print("")
                print("")
                print(f"Processing commit: {commit}")

            if not hasattr(commit, 'ops'):
                return

            for op in commit.ops:

                #type_action = classify_type_action(op.path, self.action_classifier)

                data_to_save = self._extract_metadata(commit, op, resolver)

                if self.verbose:
                    print(f"Processing op: {op}")

                new_data = self._process_CAR_data(commit, op)

                data_to_save.update(new_data)
                self._save_data(data_to_save, output_file)


        except Exception as e:
            print(f"Error processing action: {e}")

    def _extract_metadata (self, commit, op, resolver):
        author_handle = self._resolve_author_handle(commit.repo, resolver)
        timestamp = commit.time
        action = op.action

        return {
            'author': author_handle,
            'timestamp': timestamp,
            'action': action,
        }

    def _process_CAR_data(self, commit, op):
        ACTION_HANDLERS = {
            'app.bsky.feed.post': '_extract_post_data',
            'app.bsky.feed.like': '_extract_like_data',
            'app.bsky.feed.repost': '_extract_repost_data',
            'app.bsky.graph.follow': '_extract_follow_data',
            'app.bsky.graph.block': '_extract_block_data',
            "app.bsky.feed.threadgate" : "_extract_thread_data",
            "app.bsky.labeler.service" : "_extract_labeler_data",
            "app.bsky.feed.postgate" : "_extract_postgate_data",
            "place.stream.broadcast.origin" : "_extract_origin_data",
            "app.bsky.actor.status" : "_extract_actor_data",
            "chat.bsky.actor.declaration" : "_extract_declaration_data",
            "app.bsky.actor.profile" : "_extract_profile_data",
            "app.bsky.feed.generator" : "_extract_generator_data",
            "app.bsky.graph.listitem" : "_extract_listitem_data",
            'app.bsky.graph.starterpack' : '_extract_starterpack_data',
            'app.bsky.graph.listblock' : '_extract_listblock_data',
            'app.bsky.graph.list' : '_extract_list_data',
            # Add more actions as needed
        }
        """Process a single post operation"""
        try:
            car = CAR.from_bytes(commit.blocks)
            if self.verbose:
                print(f"Processing car: {car}")
                print(f"Processing car.blocks: {car.blocks}")
                print(f"Processing car.blocks.values() : {car.blocks.values()}")
            for record in car.blocks.values():

                if self.verbose:
                    print(f"Processing record: {record}")

                if isinstance(record, dict):
                    type_action = record.get('$type')

                    if type_action:
                        print(f"Processing type_action: {type_action}")

                        handler_name = ACTION_HANDLERS.get(type_action)

                        if handler_name:

                            handler_method = getattr(self, handler_name)
                            return handler_method(record, commit.repo, op.path, type_action)

            return {}
        
        except Exception as e:
            print(f"Error processing record: {e}")

    def _resolve_author_handle(self, repo, resolver):
        """Resolve the author handle from the DID"""
        try:
            resolved_info = resolver.did.resolve(repo)
            return resolved_info.also_known_as[0].split('at://')[1] if resolved_info.also_known_as else repo
        except Exception as e:
            print(f"Could not resolve handle for {repo}: {e}")
            return repo  # Fallback to DID

    def _extract_post_data(self,record, repo, path, typeof_action):
        """Extract post data from a record"""
        has_images = self._check_for_images(record)
        reply_to = self._get_reply_to(record)
        return {
            'text': record.get('text', ''),
            'uri': f'at://{repo}/{path}',
            'has_images': has_images,
            'reply_to': reply_to,
            'typeOfAction': typeof_action,
            'lang': record.get('langs', ''),
        }

    def _extract_like_data(self,record, repo, path, typeof_action):
        print("LIKE")
        print(record)
        return record

    def _extract_repost_data(self,record, repo, path, typeof_action):
        print("REPOST")
        print(record)
        return record

    def _extract_block_data(self,record, repo, path, typeof_action):
        print("BLOCK")
        print(record)
        return record

    def _extract_follow_data(self,record, repo, path, typeof_action):
        print("FOLLOW")
        print(record)
        return record

    def _extract_origin_data(self,record, repo, path, typeof_action):
        print("ORIGIN")
        print(record)
        return record
    def _extract_actor_data(self,record, repo, path, typeof_action):
        print("ACTOR")
        print(record)
        return record
    def _extract_declaration_data(self,record, repo, path, typeof_action):
        print("DECLARATION")
        print(record)
        return record
    def _extract_profile_data(self,record, repo, path, typeof_action):
        print("PROFILE")
        print(record)
        return record
    def _extract_generator_data(self,record, repo, path, typeof_action):
        print("GENERATOR")
        print(record)
        return record
    def _extract_listitem_data(self,record, repo, path, typeof_action):
        print("LISTITEM")
        print(record)
        return record

    def _extract_postgate_data(self,record, repo, path, typeof_action):
        print("POSTGATE")
        print(record)
        return record

    def _extract_thread_data(self,record, repo, path, typeof_action):
        print("THREAD")
        print(record)
        return record

    def _extract_labeler_data(self,record, repo, path, typeof_action):
        print("LABELER")
        print(record)
        return record

    def _extract_starterpack_data(self,record, repo, path, typeof_action):
        print("STARTER")
        print(record)
        return record

    def _extract_listblock_data(self,record, repo, path, typeof_action):
        print("LISTBLOCK")
        print(record)
        return record

    def _extract_list_data(self,record, repo, path, typeof_action):
        print("LIST")
        print(record)
        return record


    def _check_for_images(self,record):
        """Check if the post has images"""
        embed = record.get('embed', {})
        return (
                embed.get('$type') == 'app.bsky.embed.images' or
                (embed.get('$type') == 'app.bsky.embed.external' and 'thumb' in embed)
        )

    def _get_reply_to(self,record):
        """Get the URI of the post being replied to"""
        reply_ref = record.get('reply', {})
        return reply_ref.get('parent', {}).get('uri')

    def _save_data(self, post_data, output_file):
        """Save post data to the output file"""
        with open(output_file, 'a') as f:
            json.dump(post_data, f)
            f.write('\n')

def main():
    print("Starting Firehose Scraper")

    config = Config()
    action_filename = config.get("actions.filename")
    action_save = config.get("actions.save")
    output_filename = config.get("firehose.output_file")
    verbose = config.get("firehose.verbose")
    scraping_duration = config.get("scraping.time_limit")
    scraping_limit = config.get("scraping.action_limit")

    action_classifier = ActionClassifier(action_filename, action_save)
    firehose_scraper = FirehoseScraper(action_classifier, output_filename, verbose)

    firehose_scraper.start_collection(duration_seconds=scraping_duration, post_limit=scraping_limit)

if __name__ == "__main__":
    main()

