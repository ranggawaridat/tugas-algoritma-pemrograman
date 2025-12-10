import time

class SortResult:
    def __init__(self, data, steps, complexity, time_taken):
        self.data = data
        self.steps = steps
        self.complexity = complexity
        self.time_taken = time_taken

class SortingAlgorithms:
    
    @staticmethod
    def _get_val(item, key):
        if key is None:
            return item
        if isinstance(item, dict):
            return item.get(key)
        return getattr(item, key, item)

    @staticmethod
    def _compare(val_a, val_b, ascending=True):
        """Returns True if val_a should come AFTER val_b (i.e., swap needed in bubble sort logic)"""
        # Handle case insensitive string comparison
        if isinstance(val_a, str) and isinstance(val_b, str):
            val_a = val_a.lower()
            val_b = val_b.lower()
            
        if ascending:
            return val_a > val_b
        else:
            return val_a < val_b

    @staticmethod
    def bubble_sort(arr, key=None, ascending=True):
        data = arr.copy()
        n = len(data)
        steps = 0
        start_time = time.perf_counter()
        
        for i in range(n):
            for j in range(0, n-i-1):
                steps += 1 # Comparison
                val_a = SortingAlgorithms._get_val(data[j], key)
                val_b = SortingAlgorithms._get_val(data[j+1], key)
                
                if SortingAlgorithms._compare(val_a, val_b, ascending):
                    data[j], data[j+1] = data[j+1], data[j]
                    steps += 1 # Swap
        
        end_time = time.perf_counter()
        return SortResult(
            data, 
            steps, 
            "O(n^2)", 
            f"{(end_time - start_time) * 1000:.4f} ms"
        )

    @staticmethod
    def selection_sort(arr, key=None, ascending=True):
        data = arr.copy()
        n = len(data)
        steps = 0
        start_time = time.perf_counter()
        
        for i in range(n):
            target_idx = i
            for j in range(i+1, n):
                steps += 1 # Comparison
                val_j = SortingAlgorithms._get_val(data[j], key)
                val_target = SortingAlgorithms._get_val(data[target_idx], key)
                
                # For selection sort:
                # Ascending: find MIN (if val_j < val_target, update target)
                # Descending: find MAX (if val_j > val_target, update target)
                # equivalent to: if NOT compare(val_j, val_target, ascending) -> logic invalid for compare func above
                # Let's write explicit logic:
                should_update = False
                if isinstance(val_j, str) and isinstance(val_target, str):
                    val_j = val_j.lower()
                    val_target = val_target.lower()

                if ascending:
                    if val_j < val_target: should_update = True
                else:
                    if val_j > val_target: should_update = True
                
                if should_update:
                    target_idx = j
            
            data[i], data[target_idx] = data[target_idx], data[i]
            steps += 1 # Swap
            
        end_time = time.perf_counter()
        return SortResult(data, steps, "O(n^2)", f"{(end_time - start_time) * 1000:.4f} ms")

    @staticmethod
    def insertion_sort(arr, key=None, ascending=True):
        data = arr.copy()
        steps = 0
        start_time = time.perf_counter()
        
        for i in range(1, len(data)):
            item = data[i]
            item_val = SortingAlgorithms._get_val(item, key)
            if isinstance(item_val, str): item_val = item_val.lower()

            j = i-1
            steps += 1 # Initial check
            
            while j >= 0:
                curr_val = SortingAlgorithms._get_val(data[j], key)
                if isinstance(curr_val, str): curr_val = curr_val.lower()
                
                # Ascending: while item < curr (move curr right)
                # Descending: while item > curr (move curr right)
                condition = False
                if ascending:
                     if item_val < curr_val: condition = True
                else:
                     if item_val > curr_val: condition = True
                
                if condition:
                    steps += 1 
                    data[j + 1] = data[j]
                    steps += 1 # Shift
                    j -= 1
                else:
                    break
            data[j + 1] = item
            steps += 1 # Assignment
            
        end_time = time.perf_counter()
        return SortResult(data, steps, "O(n^2)", f"{(end_time - start_time) * 1000:.4f} ms")

    @staticmethod
    def merge_sort(arr, key=None, ascending=True):
        data = arr.copy()
        steps = [0] 
        start_time = time.perf_counter()
        
        result = SortingAlgorithms._merge_sort_recursive(data, steps, key, ascending)
        
        end_time = time.perf_counter()
        return SortResult(result, steps[0], "O(n log n)", f"{(end_time - start_time) * 1000:.4f} ms")

    @staticmethod
    def _merge_sort_recursive(arr, steps, key, ascending):
        if len(arr) <= 1:
            return arr
            
        mid = len(arr) // 2
        left = SortingAlgorithms._merge_sort_recursive(arr[:mid], steps, key, ascending)
        right = SortingAlgorithms._merge_sort_recursive(arr[mid:], steps, key, ascending)
        
        return SortingAlgorithms._merge(left, right, steps, key, ascending)

    @staticmethod
    def _merge(left, right, steps, key, ascending):
        sorted_arr = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            steps[0] += 1 # Comparison
            
            val_a = SortingAlgorithms._get_val(left[i], key)
            val_b = SortingAlgorithms._get_val(right[j], key)
            if isinstance(val_a, str) and isinstance(val_b, str):
                val_a = val_a.lower()
                val_b = val_b.lower()
            
            condition = False
            if ascending:
                if val_a < val_b: condition = True
            else:
                if val_a > val_b: condition = True

            if condition:
                sorted_arr.append(left[i])
                i += 1
            else:
                sorted_arr.append(right[j])
                j += 1
            steps[0] += 1 # Append
        
        sorted_arr.extend(left[i:])
        steps[0] += len(left[i:])
        sorted_arr.extend(right[j:])
        steps[0] += len(right[j:])
        
        return sorted_arr

    @staticmethod
    def shell_sort(arr, key=None, ascending=True):
        data = arr.copy()
        n = len(data)
        gap = n // 2
        steps = 0
        start_time = time.perf_counter()
        
        while gap > 0:
            for i in range(gap, n):
                temp = data[i]
                temp_val = SortingAlgorithms._get_val(temp, key)
                if isinstance(temp_val, str): temp_val = temp_val.lower()
                
                j = i
                steps += 1 
                
                while j >= gap:
                    gap_val = SortingAlgorithms._get_val(data[j - gap], key)
                    if isinstance(gap_val, str): gap_val = gap_val.lower()
                    
                    # Ascending: while gap_val > temp (move gap_val right)
                    # Descending: while gap_val < temp (move gap_val right)
                    condition = False
                    if ascending:
                         if gap_val > temp_val: condition = True
                    else:
                         if gap_val < temp_val: condition = True
                    
                    if condition:
                        steps += 1
                        data[j] = data[j - gap]
                        j -= gap
                    else:
                        break
                data[j] = temp
                steps += 1
            gap //= 2
            
        end_time = time.perf_counter()
        return SortResult(data, steps, "O(n log n) - O(n^2)", f"{(end_time - start_time) * 1000:.4f} ms")
