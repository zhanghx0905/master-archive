/*
 * Bonus task: Add at most five JUnit 5 crashing test cases that are not included in the "test" folder.
 * For each crashing test case, comment clearly which program statement in Util is the root cause of the crash.
 * Make corresponding amendment to Util_Fixed class.
 */
import static org.junit.jupiter.api.Assertions.*;

import java.time.Duration;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;

class UtilCrashingTest {

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
	void testMergeOverlap() {
		Util util = new Util();
		int[] arr2 = new int[] {0};
		util.mergeWithExtraStorage(0, 1, 0, 1, arr2);
	}

	@Test
	void testFindMin() {
		Util util = new Util();
		int[] arr1 = new int[] {0};
		util.findMinViaIteration(arr1);
	}
	
	@Test
	void testQuickSelectDeadLoop() {
		Util util = new Util();
		int[] arr2 = new int[] {0, 1};
		Duration d = Duration.ofSeconds(1);
		assertTimeoutPreemptively(d, () -> {util.findKthViaQuickSort(1, arr2, 1, 0);});
	}
}
