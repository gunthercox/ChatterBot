class FixedSizeQueue(object):
    """
    This is a data structure like a queue.
    Only a fixed number of items can be added.
    Once the maximum is reached, when a new item is
    added the oldest item in the queue will be removed.
    """

    def __init__(self, maxsize=10):
        self.maxsize = maxsize
        self.queue = []

    def append(self, item):
        """
        Append an element at the end of the queue.
        """
        if len(self.queue) == self.maxsize:
            # Remove an element from the top of the list
            self.queue.pop(0)

        self.queue.append(item)

    def __len__(self):
        return len(self.queue)

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

    def peek(self):
        """
        Return the most recent item put in the queue.
        """
        if self.empty():
            return None
        return self.queue[-1]

    def flush(self):
        """
        Remove all elements from the queue.
        """
        self.queue = []
