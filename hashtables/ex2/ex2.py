#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


class Ticket:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination


def reconstruct_trip(tickets, length):
    hashtable = HashTable(length)
    route = [None] * length

    """
    YOUR CODE HERE
    """
    current = 0 
    for ticket in tickets:
        # Fill hash table
        hash_table_insert(hashtable, ticket.source, ticket.destination)
        
        # Set current by finding None value
        if ticket.source == 'NONE' or ticket.source == 'none' or ticket.source == 'None':
            route[current] = ticket.destination
            current += 1
    

    while current < length: 
        print(hash_table_retrieve(hashtable, route[current - 1]))
        route[current] = hash_table_retrieve(hashtable, route[current - 1])
        current += 1

    print(route)
    return route

TEST_tickets = [
    Ticket("PIT", "ORD"),
    Ticket("XNA", "SAP"),
    Ticket("SFO", "BHM"),
    Ticket("FLG", "XNA"),
    Ticket("NONE", "LAX"),
    Ticket("LAX", "SFO"),
    Ticket("SAP", "SLC"),
    Ticket("ORD", "NONE"),
    Ticket("SLC", "PIT"),
    Ticket("BHM", "FLG"),
]
length = 10
reconstruct_trip(TEST_tickets, length)
