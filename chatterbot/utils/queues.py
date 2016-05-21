class ResponseQueue(object):
    """
    This is a data structure like a queue.
    Only a fixed number of items can be added.
    Once the maximum is reached, when a new item
    is added the oldest item in the queue will
    be removed.
    """

    def __init__(self, maxsize=10):
        self.maxsize = maxsize
        self.queue = []

    def append(self, item):
        if len(self.queue) == self.maxsize:
            # Remove an element from the top of the list
            self.queue.pop(0)

        self.queue.append(item)

    def __getitem__(self, index):
        return self.queue[index]

    def __contains__(self, item):
        """
        Check if an element is in this queue.
        """
        return item in self.queue

    def empty(self):
        """
        Return True if the queue is empty, False otherwise.
        """
        return len(self.queue) == 0
