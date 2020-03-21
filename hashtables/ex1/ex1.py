#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


def get_indices_of_item_weights(weights, length, limit):
    ht = HashTable(16)

    """
    YOUR CODE HERE
    """

     # Fill Hash Table
    for i in range(len(weights)):
        hash_table_insert(ht, weights[i], i)

    # Single Pass Loop
    for i in range(len(weights)):
        # What number is needed for this weight
        num_needed = limit - weights[i]
        index = None

        # O(1) check if the number we need is already in the HashTable
        if hash_table_retrieve(ht, num_needed):
            index = i
            num_needed = hash_table_retrieve(ht, num_needed)

            # Set appropriate positions
            if index > num_needed:
                return (index, num_needed)
            else:
                return (num_needed, index)

    return None


def print_answer(answer):
    if answer is not None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")
