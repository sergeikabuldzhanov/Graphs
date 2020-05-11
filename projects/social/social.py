from random import randrange
from queue import SimpleQueue


class User:
    def __init__(self, name):
        self.name = name


class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        # Add users
        for user in range(num_users):
            self.add_user(user)

        # Create friendships
        # for every user
        for user in self.users:
            # assign random number of friendships
            friends_num = randrange(avg_friendships*2)
            for _ in range(friends_num):
                # assign other random users as friends
                friend_id = randrange(num_users)
                if user < friend_id:
                    self.add_friendship(user, friend_id)

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME
        paths = SimpleQueue()
        paths.put(user_id)
        # store a queue of paths
        while not paths.empty():
            current = paths.get()
            if current not in visited:
                visited[current] = [current]
            # else, look at all the neghbours, and add new paths to the queue
            for adjacent in self.friendships[current]:
                if adjacent not in visited:
                    paths.put(adjacent)
                    new_path = visited[current]+[adjacent]
                    visited[adjacent] = new_path
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(1000, 5)
    # print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    # print(connections)
    degrees = 0
    for connection in connections:
        degrees += len(connections[connection])
    print(degrees/len(connections))
