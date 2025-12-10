import time

class SearchResult:
    def __init__(self, index, steps, complexity, time_taken, found):
        self.index = index
        self.steps = steps
        self.complexity = complexity
        self.time_taken = time_taken
        self.found = found

class SearchingAlgorithms:

    @staticmethod
    def _get_val(item, key):
        if key is None:
            return item
        if isinstance(item, dict):
            return item.get(key)
        return getattr(item, key, item)

    @staticmethod
    def linear_search(data, target, key=None):
        steps = 0
        start_time = time.perf_counter()
        
        target_str = str(target).lower() if isinstance(target, str) else str(target)
        
        for i, item in enumerate(data):
            steps += 1
            val = SearchingAlgorithms._get_val(item, key)
            val_str = str(val).lower() if isinstance(val, str) else str(val)
            
            if val_str == target_str:
                end_time = time.perf_counter()
                return SearchResult(i, steps, "O(n)", f"{(end_time - start_time) * 1000:.4f} ms", True)
        
        end_time = time.perf_counter()
        return SearchResult(-1, steps, "O(n)", f"{(end_time - start_time) * 1000:.4f} ms", False)

    @staticmethod
    def sequential_search(data, target, key=None):
        """Alias for Linear Search as requested."""
        return SearchingAlgorithms.linear_search(data, target, key)

    @staticmethod
    def binary_search(data, target, key=None):
        # Assumes data is sorted by the SAME key
        steps = 0
        start_time = time.perf_counter()
        
        left = 0
        right = len(data) - 1
        
        # Normalize target for comparison
        # We need careful typing here. 
        # If target matches the type of the key field, great. 
        # If not, comparison might be tricky. 
        # For simplicity, we try to cast target to type of mid_val, or fallback to string comparison.
        
        while left <= right:
            steps += 1
            mid = (left + right) // 2
            
            mid_item = data[mid]
            mid_val = SearchingAlgorithms._get_val(mid_item, key)
            
            # Comparison Logic
            try:
                # Try strict comparison if types match or are compatible numbers
                tgt_val = type(mid_val)(target)
                
                # Case insensitive string
                if isinstance(mid_val, str):
                    mid_val_c = mid_val.lower()
                    tgt_val_c = tgt_val.lower()
                else:
                    mid_val_c = mid_val
                    tgt_val_c = tgt_val
                    
                if mid_val_c == tgt_val_c:
                    end_time = time.perf_counter()
                    return SearchResult(mid, steps, "O(log n)", f"{(end_time - start_time) * 1000:.4f} ms", True)
                elif mid_val_c < tgt_val_c:
                    left = mid + 1
                else:
                    right = mid - 1
            except:
                # Fallback to loose string comparison
                mid_str = str(mid_val).lower()
                tgt_str = str(target).lower()
                
                if mid_str == tgt_str:
                    end_time = time.perf_counter()
                    return SearchResult(mid, steps, "O(log n)", f"{(end_time - start_time) * 1000:.4f} ms", True)
                elif mid_str < tgt_str:
                    left = mid + 1
                else:
                    right = mid - 1
                
        end_time = time.perf_counter()
        return SearchResult(-1, steps, "O(log n)", f"{(end_time - start_time) * 1000:.4f} ms", False)
