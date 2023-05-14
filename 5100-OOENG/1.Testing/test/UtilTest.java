/*
 * Task 2:
 * Add JUnit 5 test cases designed by you to the UtilTest class increasing the test coverage. 
 * These test cases must not be generated.
 */
import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class UtilTest {

	@BeforeAll
	static void setUpBeforeClass() throws Exception {
	}

	@AfterAll
	static void tearDownAfterClass() throws Exception {
	}

	@BeforeEach
	void setUp() throws Exception {
	}

	@AfterEach
	void tearDown() throws Exception {
	}

	@Test
	void testInvalid() {
		Util util = new Util();
		int[] arr = new int[] {};
		int[] arr1 = new int[] {1};
		
		assertTrue(util.invalidArrayAccess(arr, -1));
		assertTrue(util.invalidArrayAccess(arr, 2));
		
		util.swap(null, -1, -1);
		
		util.MergeSort(null);
		util.MergeSort(0, 0, null);
		util.mergeWithExtraStorage(0, 0, 0, 0, null);
		
		util.reverse(null, 0, 0);
		util.getNextPermutationNumber(arr);
		
//		util.findMinViaIteration(null);
		util.findMinViaIteration(arr);
		util.findKthViaQuickSort(1, null, 0, 0);
		util.findKthViaQuickSort(0, null, 0, 0);
		assertEquals(util.removeDuplicateElements(arr), 0);
		
		assertEquals(util.findMinSubArrayLen(0, arr), 0);
		assertEquals(util.findMinSubArrayLen(0, arr1), 0);
		
		assertEquals(util.findMinViaRecursion(null, 0, 0), -1);
		assertEquals(util.findMinViaRecursion(null), -1);
		assertEquals(util.findMinViaRecursion(arr1, 0, 0), 1);
	}

	@Test
	void testMin() {
		Util util = new Util();
		assertEquals(util.min(1, 2), 1);
		assertEquals(util.min(2, 1), 1);
	}
	
	@Test
	void testFindMin() {
		Util util = new Util();
		int[] arr = new int[] {4,5,6,7,0,1,2};
		assertEquals(util.findMinViaRecursion(arr), 0);
		int[] arr1 = new int[] {4, 5, 6};
		assertEquals(util.findMinViaRecursion(arr1), 4);
	}
	
	@Test
	void testFindKth() {
		Util util = new Util();
		int[] arr = new int[] {3, 1, 2, 4};
		assertEquals(util.findKthLargestViaQuickSort(arr, 2), 3);
		int[] arr1 = new int[] {4, 3, 2 ,1};
		assertEquals(util.findKthLargestViaQuickSort(arr, 2), 3);
	}
	
	
	@Test
	void testThreeSum() {
		Util util = new Util();
		int[] arr = new int[] {0, 0, 0};
		util.threeSumClosest(arr, Integer.MAX_VALUE);
	}
	
}
