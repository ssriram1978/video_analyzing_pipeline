import time
import os
import sys
from sys import path

path.append(os.getcwd())

import time

from kafka_post.kafka_producer import post_filename_to_a_kafka_topic

from log.log_file import logging_to_console_and_syslog

def process_new_file(file_name):
    # post the file_name into a kafka topic kafka_topic_name
    post_filename_to_a_kafka_topic(file_name)


def watch_a_directory(video_file_path):
    before = dict([(f, None) for f in os.listdir(video_file_path)])
    while 1:
        time.sleep(1)
        after = dict([(f, None) for f in os.listdir(video_file_path)])
        added = [f for f in after if not f in before]
        removed = [f for f in before if not f in after]
        if added:
            logging_to_console_and_syslog("Added: " + str(added))
            for filename in added:
                process_new_file(video_file_path + '/' + filename)
        if removed:
            logging_to_console_and_syslog("Removed: " + str(removed))
        before = after


if __name__ == "__main__":
    try:
        # if proceed_with_execution() == True:
        video_file_path = os.getenv("video_file_path_key", default=None)
        logging_to_console_and_syslog(("video_file_path={}".format(video_file_path)))
        # watch_a_directory(video_file_path)
        watch_a_directory(video_file_path)
    except NoProcessExcept as e:
        logging_to_console_and_syslog(("No Process exception occurred.{}".format(e)))
    except KeyboardInterrupt:
        logging_to_console_and_syslog("You terminated the program by pressing ctrl + c")
    except BaseException:
        logging_to_console_and_syslog("Base Exception occurred")
    except:
        logging_to_console_and_syslog("Unhandled exception")
    finally:
        exit