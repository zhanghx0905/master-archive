/*
 * Task 3: Add at most five JUnit 5 test cases to reveal four distinct program faults in Util.
 * Add comments in each failing test case the line in Util.java that is the root cause of the failure.
 * Make corresponding amendment to the Util_Fixed class.
 */
import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class UtilFailingTest {

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
	void testRemoveDuplicateError() {
		// line 172  A[o++] = curr;
		Util util = new Util();
		int[] arr = new int[] {1, 1, 2};
		util.removeDuplicateElements(arr);
		assertEquals(arr[0], 1);
		assertEquals(arr[1], 2);
	}
	
	@Test
	void testFindSubError1() {
		// line 202 if (nums.length == 1 || nums[0] < s) {
		Util util = new Util();
		int[] arr = new int[] {2,3,1,2,4,3};
		assertEquals(util.findMinSubArrayLen(7, arr), 2);
	}
	
	@Test
	void testFindSubError2() {
		// line 234 if (i < 0) {
		Util util = new Util();
		int[] arr = new int[] {1,1,1,1,1,1,1,1};
		assertEquals(util.findMinSubArrayLen(11, arr), 8);
	}

	@Test
	void testPermError() {
		// line 286 if (p == 0 || q == 0) {
		Util util = new Util();
		int[] arr = new int[] {1,3,2};
		int[] ans = new int[] {2,1,3};
		util.getNextPermutationNumber(arr);
		assertArrayEquals(arr, ans);
	}
	
	@Test
	void testThreeSumError() {
		// line 337 if (diff >= min) {
		Util util = new Util();
		int[] arr = new int[] {-1, 2, 1, 4};
		assertEquals(util.threeSumClosest(arr, 1), 2);
	}
	
}
