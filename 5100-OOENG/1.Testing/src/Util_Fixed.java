/* 
 * Task 3: Please comment out the faulty statements that your test cases have detected.
 * Replace the faulty statements with the appropriate fixed statements.
 * Clearly index each fix with the name of the test method that detects the failure.
 */
public class Util_Fixed {
	/**
	 * Check whether the array access is valid.
	 * @param arr
	 * @param indices
	 * @return true if array is not null and all indices are within the index range.
	 */
	boolean invalidArrayAccess(int[] arr, int ...indices) {
		if (arr == null) return true;
		for (var index: indices) {
			if (index < 0 || index >= arr.length) 
				return true;
		}
		return false;
	}
	
	/**
	 * get the k-th largest value of an integer array
	 * 
	 * Example: the 4-th largest value of [4,5,2,6,2] is 2.
	 * 
	 * @param nums  the array to search
	 * @param k  the k-th
	 * @return   
	 */
	public int findKthLargestViaQuickSort(int[] nums, int k) {
		if (k < 1 || invalidArrayAccess(nums) || k > nums.length) {
			return 0;
		}

		return findKthViaQuickSort(nums.length - k + 1, nums, 0, nums.length - 1);
	}

	int findKthViaQuickSort(int k, int[] nums, int start, int end) {
//		if (k < 1 || invalidArrayAccess(nums, start, end))
		if (k < 1 || invalidArrayAccess(nums, start, end) || start > end)	// testQuickSelectDeadLoop (BONUS)
			return 0;

		int pivot = nums[end];

		int left = start;
		int right = end;

		while (true) {

			while (nums[left] < pivot && left < right) {
				left++;
			}

			while (nums[right] >= pivot && right > left) {
				right--;
			}

			if (left == right) {
				break;
			}

			swap(nums, left, right);
		}

		swap(nums, left, end);

		if (k == left + 1) {
			return pivot;
		} else if (k < left + 1) {
			return findKthViaQuickSort(k, nums, start, left - 1);
		} else {
			return findKthViaQuickSort(k, nums, left + 1, end);
		}
	}

	void swap(int[] nums, int n1, int n2) {
		if (invalidArrayAccess(nums, n1, n2)) 
			return;
		int tmp = nums[n1];
		nums[n1] = nums[n2];
		nums[n2] = tmp;
	}

	/**
	 * get the minimal value of an array through recursion way
	 * @param num
	 * @return
	 */
	int findMinViaRecursion(int[] num) {
		if (invalidArrayAccess(num)) 
			return -1;
		return findMinViaRecursion(num, 0, num.length - 1);
	}
	
	int findMinViaRecursion(int[] num, int left, int right) {
		if (invalidArrayAccess(num, left, right)) 
			return -1;
		if (left == right)
			return num[left];
		if ((right - left) == 1)
			return min(num[left], num[right]);

		int middle = left + (right - left) / 2;

		// not rotated
		if (num[left] < num[right]) {
			return num[left];

			// go right side
		} else if (num[middle] > num[left]) {
			return findMinViaRecursion(num, middle, right);

			// go left side
		} else {
			return findMinViaRecursion(num, left, middle);
		}
	}
	
	/**
	 * find the minimal value of an array through iteration
	 * @param nums
	 * @return
	 */
	public int findMinViaIteration(int[] nums) {
		if (invalidArrayAccess(nums) || nums.length == 0)
			return -1;

		if (nums.length == 1)
			// return nums[1];
			return nums[0];		// testFindMin (BONUS)

		int left = 0;
		int right = nums.length - 1;

		// not rotated
		if (nums[left] < nums[right])
			return nums[left];

		while (left <= right) {
			if (right - left == 1) {
				return nums[right];
			}

			int m = left + (right - left) / 2;

			if (nums[m] > nums[right])
				left = m;
			else
				right = m;
		}

		return nums[left];
	}
	
	/**
	 * remove duplicate elements in an array
	 * @param A
	 * @return
	 */
	public int removeDuplicateElements(int[] A) {
		if (invalidArrayAccess(A) || A.length == 0)
			return 0;

		int pre = A[0];
		boolean flag = false;
		int count = 0;

		// index for updating
		int o = 1;

		for (int i = 1; i < A.length; i++) {
			int curr = A[i];

			if (curr == pre) {
				if (!flag) {
					flag = true;
//					A[o++] = curr;	// testRemoveDuplicateError

					continue;
				} else {
					count++;
				}
			} else {
				pre = curr;
				A[o++] = curr;
				flag = false;
			}
		}

		return o;
	}

	/**
	 * Find the minimal length of a subarray 
	 * of which the sum is NOT smaller than a given value
	 * 
	 * Example: given value 10, this method will return 2 for array [1,3,5,7,3] 
	 * 
	 * @param s
	 * @param nums
	 * @return
	 */
	public int findMinSubArrayLen(int s, int[] nums) {
		if(invalidArrayAccess(nums) || nums.length == 0){
	        return 0;
	    }
		// if(nums.length == 1 || nums[0] < s){
	    if(nums.length == 1 && nums[0] < s){	// testFindSubError1
	        return 0;
	    }
	    int result = nums.length;
	 
	    int i = 0;
	    int sum = nums[0];
	 
	    for(int j=0; j<nums.length; ){
	        if(i==j){
	            if(nums[i]>=s){ 
	                return 1;
	            }else{
	               j++;
	 
	               if(j<nums.length){
	                    sum = sum + nums[j];
	               }else{
	                    return result;
	               }
	            }    
	        }else{
	            if(sum >= s){
	                result = min(j-i+1, result);
	                sum = sum - nums[i]; 
	                i++;
	            }else{
	                j++;
	 
	                if(j<nums.length){
	                    sum = sum + nums[j];
	                }else{
						//if(i<0){ 
	                    if(i==0){ // testFindSubError2
	                        return 0;
	                    }else{    
	                        return result;
	                    }
	                }
	            }
	        }
	    }
	 
	    return result;
	}
		
	int min(int a, int b){
		if(a>=b){
			return b;
		}else{
			return a;
		}
	}
	
	/**
	 *  rearranges the integer array 
	 *  such that the new array is 
	 *  the lexicographically next greater permutation of numbers
	 *  
	 *  Example: the next permutation of arr = [1,2,3] is [1,3,2]
	 *  		 All permutations of {1,2,3} are {{1,2,3} , {1,3,2}, {2,13} , {2,3,1} , {3,1,2} , {3,2,1}}. 
	 *  		 So, the next permutation just after {1,2,3} is {1,3,2}.
	 *  
	 * @param nums
	 */
	public void getNextPermutationNumber(int[] nums) {
		if(invalidArrayAccess(nums) || nums.length<2)
	        return;
	 
	    int p=0;            
	    for(int i=nums.length-2; i>=0; i--){
	        if(nums[i]<nums[i+1]){
	            p=i;
	            break;
	        }    
	    }
	 
	    int q = 0;
	    for(int i=nums.length-1; i>p; i--){
	        if(nums[i]> nums[p]){
	            q=i;
	            break;
	        }    
	    }
	
		// if(p==0 || q==0){
	    if(p==0 && q==0){	// testPermError
	        reverse(nums, 0, nums.length-1);
	        return;
	    }
	 
	    int temp=nums[p];
	    nums[p]=nums[q];
	    nums[q]=temp;
	 
	    if(p<nums.length-1){
	        reverse(nums, p+1, nums.length-1);
	    }
	}
	 
	void reverse(int[] nums, int left, int right){
		if (invalidArrayAccess(nums, left, right))
			return;
	    while(left<right){
	        int temp = nums[left];
	        nums[left]=nums[right];
	        nums[right]=temp;
	        left++;
	        right--;
	    }
	}	
	
	/**
	 * Select 3 numbers from an array such that
	 * their sum value is closest to the target value
	 * 
	 * @param nums
	 * @param target
	 * @return
	 */
	public int threeSumClosest(int[] nums, int target) {
		if (invalidArrayAccess(nums)) 
			return 0;
	    int min = Integer.MAX_VALUE;
		int result = 0;
	 
		MergeSort(nums);
	 
		for (int i = 0; i < nums.length; i++) {
			int j = i + 1;
			int k = nums.length - 1;
			while (j < k) {
				int sum = nums[i] + nums[j] + nums[k];
				int diff = abs(sum - target);
	 
				if(diff == 0) return sum;

				// if (diff >= min) {
				if (diff < min) {	// testThreeSumError
					min = diff;
					result = sum;
				}
				if (sum <= target) {
					j++;
				} else {
					k--;
				}
			}
		}
	 
		return result;
	}
	
	int abs(int a){
		if(a<0){
			return -a;
		}else{
			return a;
		}
	}
	
    void MergeSort(int[] unsorted) {
    	if (invalidArrayAccess(unsorted)) 
			return;
        MergeSort(0, unsorted.length, unsorted);        
    }

    void MergeSort(int start, int length, int[] unsorted) {
    	if (invalidArrayAccess(unsorted, start, start+length-1)) 
			return;
        if (length > 2) {
            int aLength = (int) Math.floor(length / 2);
            int bLength = length - aLength;
            MergeSort(start, aLength, unsorted);
            MergeSort(start + aLength, bLength, unsorted);
            mergeWithExtraStorage(start, aLength, start + aLength, bLength, unsorted);
        } else if (length == 2) {
            int e = unsorted[start + 1];
            if (e<unsorted[start]) {
                unsorted[start + 1] = unsorted[start];
                unsorted[start] = e;
            }
        }
    }
    
    void mergeWithExtraStorage(int aStart, int aLength, int bStart, int bLength, int[] unsorted) {
    	if (invalidArrayAccess(unsorted, aStart, aStart+aLength-1, bStart, bStart+bLength-1)) 
			return;
        int count = 0;
        Integer[] output = new Integer[aLength + bLength];
        int i = aStart;
        int j = bStart;
        int aSize = aStart + aLength;
        int bSize = bStart + bLength;
        while (i < aSize || j < bSize) {
            Integer a = null;
            if (i < aSize) {
                a = unsorted[i];
            }
            Integer b = null;
            if (j < bSize) {
                b = unsorted[j];
            }
            if (a != null && b == null) {
                output[count++] = a;
                i++;
            } else if (b != null && a == null) {
                output[count++] = b;
                j++;
            } else if (b != null && b.compareTo(a) <= 0) {
                output[count++] = b;
                j++;
            } else {
                output[count++] = a;
                i++;
            }
        }
        int x = 0;
        int size = aStart + aLength + bLength;
        for (int y = aStart; y < size; y++) {
            unsorted[y] = output[x++];
        }
    }
}