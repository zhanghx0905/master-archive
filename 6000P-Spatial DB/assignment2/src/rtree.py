"""20932780 Zhang Hexiao"""

import itertools
import math
from dataclasses import dataclass, field
from typing import Callable, Optional
from collections import deque

import numpy as np
from shapely import Polygon

from rect import Rect, union_all


@dataclass
class RTreeEntry:
    rect: Rect
    data: Optional[Polygon] = None  # None for non-leaf nodes
    child: Optional["RTreeNode"] = None


@dataclass
class RTreeNode:
    tree: "RTree"
    is_leaf: bool
    parent: Optional["RTreeNode"] = None
    entries: list[RTreeEntry] = field(default_factory=list)

    @property
    def is_root(self) -> bool:
        return self.parent is None

    @property
    def parent_entry(self) -> Optional[RTreeEntry]:
        if self.parent is not None:
            return next(entry for entry in self.parent.entries if entry.child is self)
        return None

    def get_bounding_rect(self):
        return union_all([entry.rect for entry in self.entries])


class RTree:
    def __init__(self, fanout: int, max_entries: int) -> None:
        self.fanout = fanout  # for non-leaf
        self.max_entries = max_entries  # for leaf
        self.min_entries = math.ceil(max_entries / 2)
        self.root = RTreeNode(self, True)

    def insert(self, data: Polygon, mbr: Rect):
        """
        Strategy for inserting a new entry into the tree.
        First, choose the best leaf where the new entry should be inserted.
        If the node is overflowing after inserting the entry,
        then overflow_strategy is invoked.

        :param tree: R-tree instance
        :param data: Entry data
        :param rect: Bounding rectangle
        :return: RTreeEntry instance for the newly-inserted entry.
        """
        entry = RTreeEntry(mbr, data)

        # choose the leaf
        node = self.root
        while not node.is_leaf:
            e: RTreeEntry = least_area_enlargement(node.entries, entry.rect)
            node = e.child
            assert node is not None
        node.entries.append(entry)

        # split full leaf if needed
        split_node = None
        if len(node.entries) > self.max_entries:
            split_node = self.overflow_strategy(node)

        # propagate up the changes
        self.adjust_tree(node, split_node)
        return entry

    def adjust_tree(self, node: RTreeNode, split_node: Optional[RTreeNode] = None):
        """
        Ascend from a leaf node to the root, adjusting covering rectangles
        and propagating node splits as necessary.
        """
        while not node.is_root:
            parent = node.parent
            node.parent_entry.rect = union_all([entry.rect for entry in node.entries])
            if split_node is not None:
                rect = union_all([e.rect for e in split_node.entries])
                entry = RTreeEntry(rect, child=split_node)
                parent.entries.append(entry)
                if len(parent.entries) > self.fanout:
                    split_node = self.overflow_strategy(parent)
                else:
                    split_node = None
            node = parent
        if split_node is not None:
            self.grow_tree([node, split_node])

    def overflow_strategy(self, node):
        return quadratic_split(self, node)

    def perform_node_split(
        self, node: RTreeNode, group1: list[RTreeEntry], group2: list[RTreeEntry]
    ) -> RTreeNode:
        """
        Splits a given node into two nodes.
        The original node will have the entries specified in group1, and the
        newly-created split node will have the entries specified in group2.
        Both the original and split node will
        have their children nodes adjusted so they have the correct parent.

        :param node: Original node to split
        :param group1: Entries to assign to the original node
        :param group2: Entries to assign to the newly-created split node
        :return: The newly-created split node
        """
        node.entries = group1
        split_node = RTreeNode(self, node.is_leaf, parent=node.parent, entries=group2)

        def _fix_children(node: RTreeNode):
            if not node.is_leaf:
                for entry in node.entries:
                    entry.child.parent = node

        _fix_children(node)
        _fix_children(split_node)
        return split_node

    def grow_tree(self, nodes: list[RTreeNode]):
        """
        Grows the R-Tree by creating a new root node, with the given nodes as children.
        :param nodes: Existing nodes that will become children of the new root node.
        :return: New root node
        """
        entries = [RTreeEntry(node.get_bounding_rect(), child=node) for node in nodes]
        self.root = RTreeNode(self, False, entries=entries)
        for node in nodes:
            node.parent = self.root
        return self.root

    def traverse_bfs(
        self,
        fn: Callable[[RTreeNode], None],
        condition: Optional[Callable[[RTreeNode], bool]] = None,
    ):
        """
        Traverses the nodes of the R-Tree in level-order (breadth first), calling the given function on each node. For a
        depth-first traversal, use the traverse method instead. A condition function may optionally be passed to filter
        which nodes get traversed. If condition returns False, then neither the node nor any of its descendants will be
        traversed.
        :param fn: Function to execute on each node. This function should accept the node, and optionally the current
            level (with 0 corresponding to the root level) as parameters. The function should yield its result.
        :param condition: Optional condition function to evaluate on each node. The condition function should accept a
            node and a level parameter. If condition returns False, then neither the node nor any of its descendants
            will be traversed. If not passed in, all nodes will be traversed.
        """
        queue: deque[RTreeNode] = deque()
        queue.append(self.root)
        while queue:
            node = queue.popleft()
            if condition is None or condition(node):
                fn(node)
                if not node.is_leaf:
                    queue.extend(entry.child for entry in node.entries)

    def count_nodes(self):
        leaf, nonleaf = 0, 0

        def count(node: RTreeNode):
            nonlocal leaf, nonleaf
            if node.is_leaf:
                leaf += 1
            else:
                nonleaf += 1

        self.traverse_bfs(count)
        return leaf, nonleaf

    def window_query(self, rect: Rect, polygon: Polygon):
        cnt, tot = 0, 0

        def condition(node: RTreeNode):
            return rect.intersects(node.get_bounding_rect())

        def judge(node: RTreeNode):
            if not node.is_leaf:
                return
            nonlocal cnt, tot
            tot += len(node.entries)
            for entry in node.entries:
                if polygon.contains(entry.data):
                    cnt += 1

        self.traverse_bfs(judge, condition)
        return cnt, tot

    def tree_height(self):
        node = self.root
        cnt = 1
        while not node.is_leaf:
            node = node.entries[0].child
            cnt += 1
        return cnt


def least_area_enlargement(entries: list[RTreeEntry], rect: Rect) -> RTreeEntry:
    """
    Selects a child entry that requires least area enlargement
    for inserting an entry with the given bounding box.
    """
    areas = np.array([child.rect.area for child in entries])
    enlargements = np.array([rect.union(child.rect).area for child in entries]) - areas
    indices = np.where(enlargements == enlargements.min())[0]
    # If a single entry is a clear winner, choose that entry.
    # Otherwise, if there are multiple entries having the
    # same enlargement, choose the entry having the smallest area as a tie-breaker.
    if len(indices) == 1:
        return entries[indices[0]]
    else:
        i = np.argmin([areas[i] for i in indices])
        return entries[i]


def quadratic_split(tree: RTree, node: RTreeNode) -> RTreeNode:
    """
    :param tree: RTreeBase: R-tree instance.
    :param node: RTreeNode: Overflowing node that needs to be split.
    :return: Newly-created split node whose entries are a subset of the original node's entries.
    """
    entries = node.entries[:]
    seed1, seed2 = _pick_seeds(entries)
    entries.remove(seed1)
    entries.remove(seed2)
    group1, group2 = ([seed1], [seed2])
    rect1, rect2 = (seed1.rect, seed2.rect)
    num_entries = len(entries)
    while num_entries > 0:
        # If one group has so few entries that all the rest must be assigned to it in order for it to meet the
        # min_entries requirement, assign them and stop. (If both groups are underfull, then proceed with the
        # algorithm to determine the best group to extend.)
        len1, len2 = (len(group1), len(group2))
        group1_underfull = len1 < tree.min_entries <= len1 + num_entries
        group2_underfull = len2 < tree.min_entries <= len2 + num_entries
        if group1_underfull and not group2_underfull:
            group1.extend(entries)
            break
        if group2_underfull and not group1_underfull:
            group2.extend(entries)
            break
        # Pick the next entry to assign
        area1, area2 = rect1.area, rect2.area
        entry = _pick_next(entries, rect1, area1, rect2, area2)
        # Add it to the group whose covering rectangle will have to be enlarged the least to accommodate it.
        # Resolve ties by adding the entry to the group with the smaller area, then to the one with fewer
        # entries, then to either.
        urect1, urect2 = rect1.union(entry.rect), rect2.union(entry.rect)
        enlargement1 = urect1.area - area1
        enlargement2 = urect2.area - area2
        if enlargement1 == enlargement2:
            if area1 == area2:
                group = group1 if len1 <= len2 else group2
            else:
                group = group1 if area1 < area2 else group2
        else:
            group = group1 if enlargement1 < enlargement2 else group2
        group.append(entry)
        # Update the winning group's covering rectangle
        if group is group1:
            rect1 = urect1
        else:
            rect2 = urect2
        # Update entries list
        entries.remove(entry)
        num_entries = len(entries)
    return tree.perform_node_split(node, group1, group2)


def _pick_seeds(entries: list[RTreeEntry]):
    seeds = None
    max_wasted_area = None
    for e1, e2 in itertools.combinations(entries, 2):
        combined_rect = e1.rect.union(e2.rect)
        wasted_area = combined_rect.area - e1.rect.area - e2.rect.area
        if max_wasted_area is None or wasted_area > max_wasted_area:
            max_wasted_area = wasted_area
            seeds = (e1, e2)
    return seeds


def _pick_next(
    remaining_entries: list[RTreeEntry],
    group1_rect: Rect,
    group1_area: float,
    group2_rect: Rect,
    group2_area: float,
) -> RTreeEntry:
    max_diff = None
    result = None
    for e in remaining_entries:
        d1 = group1_rect.union(e.rect).area - group1_area
        d2 = group2_rect.union(e.rect).area - group2_area
        diff = math.fabs(d1 - d2)
        if max_diff is None or diff > max_diff:
            max_diff = diff
            result = e
    return result
