import math
import sys
import mmh3


class BloomFilter:
    def __init__(self, n, epsilon=0.1):
        """
        Parameters:
        n: int: size of data (used to determine m, size of bucket list)
        epsilon: float (default 0.01): Desired error rate. Higher epsilon -> lower m (smaller array) and vice versa

        Fields:
        size: int: Number of elements in the dataset
        (private) m: int: Size of array
        (private) k: int (default 10): Number of hash functions. 
        (private) bit_array: list(int): Array holding the bits for elements to be hashed to
        (private) n_filled: int: Number of '1' bits in the bit_array. Good for testing and metrics
        """
        self.size = n
        # Formula from Wikipedia on Optimal Hash fns
        self._m = int((-n * math.log(epsilon)) / math.pow(math.log(2), 2))
        self._k = int((self._m * math.log(2)) / n)  # Also from Wikipedia
        self._bit_array = [0] * self._m
        self._n_filled = 0

    @property
    def percentage_filled(self):
        return str(round((self._n_filled / len(self._bit_array)) * 100, 3)) + "%"

    @property
    def memory_used(self):
        return sys.getsizeof(self._bit_array)

    def add(self, element):
        """
        Adds the element to the Bloom Filter. Computes K hashes of element and stores the results in the array.
        """
        buckets = self._get_bucket_idxes(element)

        for bucket_idx in buckets:
            if self._bit_array[bucket_idx] == 0:
                self._n_filled += 1

            self._bit_array[bucket_idx] = 1

    def probabilistic_contains(self, element):
        """
        Will return true if there is a chance that the element is in the array (probabilistic), false otherwise
        """
        buckets = self._get_bucket_idxes(element)

        for bucket_idx in buckets:
            if self._bit_array[bucket_idx] == 0:
                return False

        return True

    def _get_bucket_idxes(self, element):
        idxes = []
        # Each i is a seed for a new Universal Hash Fn
        for i in range(self._k):
            idxes.append(mmh3.hash128(element, i) % len(self._bit_array))

        return idxes
