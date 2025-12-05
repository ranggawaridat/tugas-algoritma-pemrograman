from typing import List, Callable, Optional
from .models import Mahasiswa

# Fitur Pengurutan Data (Sorting)
class SortingAlgorithms:
    
    @staticmethod
    def bubble_sort(data: List[Mahasiswa], key: str = 'nim', ascending: bool = True) -> List[Mahasiswa]:
        """
        Bubble Sort: Time Complexity O(n^2)
        Membandingkan elemen bersebelahan dan menukarnya jika urutan salah.
        """
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                val_a = getattr(arr[j], key)
                val_b = getattr(arr[j+1], key)
                
                condition = (val_a > val_b) if ascending else (val_a < val_b)
                
                if condition:
                    # Swap (Pointer/Reference manipulation)
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

    @staticmethod
    def selection_sort(data: List[Mahasiswa], key: str = 'nim', ascending: bool = True) -> List[Mahasiswa]:
        """
        Selection Sort: Time Complexity O(n^2)
        Mencari elemen terkecil/terbesar dan menukarnya ke posisi awal.
        """
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            idx_target = i
            for j in range(i+1, n):
                val_target = getattr(arr[idx_target], key)
                val_current = getattr(arr[j], key)
                
                condition = (val_current < val_target) if ascending else (val_current > val_target)
                
                if condition:
                    idx_target = j
            
            arr[i], arr[idx_target] = arr[idx_target], arr[i]
        return arr

    @staticmethod
    def merge_sort(data: List[Mahasiswa], key: str = 'nim', ascending: bool = True) -> List[Mahasiswa]:
        """
        Merge Sort: Time Complexity O(n log n)
        Divide and Conquer algorithm.
        """
        if len(data) <= 1:
            return data
        
        mid = len(data) // 2
        left_half = data[:mid]
        right_half = data[mid:]
        
        left_sorted = SortingAlgorithms.merge_sort(left_half, key, ascending)
        right_sorted = SortingAlgorithms.merge_sort(right_half, key, ascending)
        
        return SortingAlgorithms._merge(left_sorted, right_sorted, key, ascending)

    @staticmethod
    def _merge(left: List[Mahasiswa], right: List[Mahasiswa], key: str, ascending: bool) -> List[Mahasiswa]:
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            val_left = getattr(left[i], key)
            val_right = getattr(right[j], key)
            
            condition = (val_left < val_right) if ascending else (val_left > val_right)
            
            if condition:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result

# Fitur Pencarian Data (Searching)
class SearchingAlgorithms:
    
    @staticmethod
    def linear_search(data: List[Mahasiswa], key: str, value: str) -> List[Mahasiswa]:
        """
        Linear/Sequential Search: Time Complexity O(n)
        Mencari data dengan menelusuri satu per satu.
        """
        results = []
        for mhs in data:
            # Case insensitive search for strings
            val_mhs = str(getattr(mhs, key)).lower()
            if str(value).lower() in val_mhs:
                results.append(mhs)
        return results

    @staticmethod
    def binary_search(data: List[Mahasiswa], target_nim: str) -> Optional[Mahasiswa]:
        """
        Binary Search: Time Complexity O(log n)
        Hanya bekerja pada data yang sudah terurut (berdasarkan NIM).
        """
        # Pastikan data terurut berdasarkan NIM sebelum binary search
        # Kita asumsikan data yang masuk ke sini sudah disortir atau kita sort dulu
        sorted_data = SortingAlgorithms.merge_sort(data, key='nim', ascending=True)
        
        low = 0
        high = len(sorted_data) - 1
        
        while low <= high:
            mid = (low + high) // 2
            mid_val = sorted_data[mid].nim
            
            if mid_val == target_nim:
                return sorted_data[mid]
            elif mid_val < target_nim:
                low = mid + 1
            else:
                high = mid - 1
        return None
