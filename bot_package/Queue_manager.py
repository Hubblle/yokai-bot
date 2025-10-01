"""
Queue manager for trade / gift command
"""


class Queue():
    """a class for a trade queue object
    """
    def __init__(self):
        self.queue = {}
    
    async def add_member(self, id : int):
        """Add a user to the queue

        Args:
            id (int): the id of the user
        """
        self.queue[id] = True

                    
    async def show(self, id : int) -> bool:
        """Return if a user is in the queue

        Args:
            id (int): the id of the user

        Returns:
            bool: If the user is in the queue
        """
        #try to see if the member has a queue (si c'est un homme je pense oui ;-)
        try : 
            qeue = self.queue[id]
        except KeyError:
            qeue = False
        return qeue

    async def delete(self, id : int):
        """Delete a user from the queue

        Args:
            id (int): The user's id
        """
        self.queue[id] = False

        