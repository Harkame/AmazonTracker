from amazontracker import AmazonTracker
import sys

if __name__ == "__main__":
    amazon_tracker = AmazonTracker()

    amazon_tracker.init(sys.argv[1:])

    amazon_tracker.run()
