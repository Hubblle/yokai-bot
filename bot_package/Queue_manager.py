"""
Queue manager for trade / gift command
"""
import discord

class Queue():
    """a class for a trade queue object
    """
    def __init__(self):
        self.queue = {}
    
    async def add_member(self, id : int, user: list[discord.User]):
        """Add a user to the queue

        Args:
            id (int): the id of the interaction
            user (list[discord.User]): the list of the users
        """
        self.queue[id]= user

                    
    async def show(self, user : discord.User) -> bool:
        """Return if a user is in the queue

        Args:
            user (discord.User): the user

        Returns:
            bool: If the user is in the queue
        """
        #try to see if the member is in the queue
        queue = False
        for interaction in self.queue:
            for users in self.queue[interaction]:
                if users.id == user.id:
                    queue = True
                    
        return queue

    async def delete(self, id : int):
        """Delete a user from the queue

        Args:
            id (int): The interaction id
        """
        try:
            self.queue.pop(id)
        except:
            pass

        