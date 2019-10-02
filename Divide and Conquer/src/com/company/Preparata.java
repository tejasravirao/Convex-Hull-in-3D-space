package com.company;

import java.util.*;

public class Preparata {

    /*
     * top and bottom are a clockwise sequence of points on the boundary of the top and bottom polygons.
     * The two sequence of points are circular. So last point's next refers to the first point.

     * The two polygons are non-intersecting along the y-axis.
     *
     * Returns right tangent of the top and bottom polygons.
     */
    private Tangent getRightTangent(Point[] top, Point[] bottom) {
        if (top == null || bottom == null) {
            return null;
        }

        Tangent result;
        int rightOfTopIdx = ConvexHullUtils.findMaxIdx(top), rightOfBottomIdx = ConvexHullUtils.findMaxIdx(bottom);
        Point rightOfTop = top[rightOfTopIdx], rightOfBottom = bottom[rightOfBottomIdx];

        double tangentSlope = ConvexHullUtils.slope(rightOfTop, rightOfBottom);
        if (rightOfTop.x > rightOfBottom.x) {
            // tangent slope is positive. tangent goes from top right to bottom left.
            while(true) {
                while(true) {
                    if(ConvexHullUtils.slope(rightOfTop, top[(rightOfTopIdx + 1) % top.length]) < tangentSlope) {
                        break;
                    }
                    rightOfTopIdx = (rightOfTopIdx + 1) % top.length;
                    rightOfTop = top[rightOfTopIdx];
                    tangentSlope = ConvexHullUtils.slope(rightOfTop, rightOfBottom);
                }
                if(ConvexHullUtils.slope(rightOfBottom, bottom[(rightOfBottomIdx + 1) % bottom.length]) <= tangentSlope) {
                    break;
                }
                rightOfBottomIdx = (rightOfBottomIdx + 1) % bottom.length;
                rightOfBottom = bottom[rightOfBottomIdx];
                tangentSlope = ConvexHullUtils.slope(rightOfTop, rightOfBottom);
            }
        } else {
            // tangent slope is negative. tangent goes from top left to bottom right.
            while (true) {
                while(true) {
                    if (ConvexHullUtils.slope(rightOfTop, top[(rightOfTopIdx + 1) % top.length]) > tangentSlope) {
                        break;
                    }
                    rightOfTopIdx = (rightOfTopIdx + 1) % top.length;
                    rightOfTop = top[rightOfTopIdx];
                    tangentSlope = ConvexHullUtils.slope(rightOfTop, rightOfBottom);
                }
                if (ConvexHullUtils.slope(rightOfBottom, bottom[(rightOfBottomIdx + 1) % bottom.length]) >= tangentSlope) {
                    break;
                }
                rightOfBottomIdx = (rightOfBottomIdx + 1) % bottom.length;
                rightOfBottom = bottom[rightOfBottomIdx];
                tangentSlope = ConvexHullUtils.slope(rightOfTop, rightOfBottom);
            }
        }

        result = new Tangent();
        result.one = rightOfTop;
        result.other = rightOfBottom;
        return result;
    }

    private class SortedAdjacent {
        Point point;
        double angle;

        SortedAdjacent(Point p, double angle) {
            this.point = p;
            this.angle = angle;
        }

        public String toString() {
            return point.toString()+" at "+angle;
        }
    }

    private SortedAdjacent[] getSortedAdjacents(Point pivot, Point axisEnd, Point current, Set<Point> adjacents) {
        return getSortedAdjacents(pivot, axisEnd, current, adjacents, false);
    }

    private SortedAdjacent[] getSortedAdjacents(Point pivot, Point axisEnd, Point current, Set<Point> adjacents, boolean isCounterClockwise) {
        // This method sorts edges based on angle in O(nlogn) time because though we use bucket-based sorting, we need to
        // sort each bucket. If all points fall in same bucket, we have O(nlogn).
        if (adjacents == null || adjacents.isEmpty()) {
            return new SortedAdjacent[0];
        }

        SortedAdjacent[] result = new SortedAdjacent[adjacents.size()];

        List<SortedAdjacent>[] bins = new List[360];
        for (Point p : adjacents) {
            double angle = ConvexHullUtils.getAngleBetweenPlanes(pivot, axisEnd, current, p, isCounterClockwise); // O(1)
            int binNumber = (int)Math.abs(angle);
            if (bins[binNumber] == null) {
                bins[binNumber] = new LinkedList<>();
            }
            bins[binNumber].add(new SortedAdjacent(p, angle));
        }
        for (int i = 0, k=0 ; i < 360 ; i++) {
            List<SortedAdjacent> binPoints = bins[i];
            if (binPoints != null) {
                // This sorting can raise the complexity to O(nlogn). Can not do anything better here.
                Collections.sort(binPoints, (o1, o2) -> o1.angle == o2.angle ? 0 : (o1.angle < o2.angle ? -1 : 1));
                for (SortedAdjacent p : binPoints) {
                    result[k++] = p;
                }
            }
        }
        return result;
    }

    private void removePointsInTriangulation(Map<Point, Set<Point>> hull, Point recent, Set<Point> pointsInTriangulation) {
        // Points already in the triangulation should not be processed again. No other vertex should have an edge to
        // triangulated point.
        Set<Point> edges = hull.getOrDefault(recent, new LinkedHashSet<>());
        Set<Point> edgesCopy = new LinkedHashSet<>(edges);
        for (Point p : edgesCopy) {
            if (pointsInTriangulation.contains(p)) {
                edges.remove(p);
                hull.get(p).remove(recent);
            }
        }
    }

    private void removeUntilMaxConvexVertex(Map<Point, Set<Point>> hullCopy,
                                            Point recent,
                                            SortedAdjacent[] sortedAdjacents,
                                            Set<Point> edges) {
        SortedAdjacent max = null;
        if (edges.size() > 0) {
            if (isConvex(sortedAdjacents[0].angle)) {
                max = sortedAdjacents[0];
                for (int i = 1; i < sortedAdjacents.length; i++) {
                    if (!isConvex(sortedAdjacents[i].angle)) {
                        break;
                    }
                    if (max.angle <= sortedAdjacents[i].angle) {
                        for (Point p : hullCopy.get(max.point)) {
                            hullCopy.get(p).remove(max.point);
                        }
                        hullCopy.get(max.point).clear();
                        max = sortedAdjacents[i];
                    }
                }
            }
        }
    }

    private boolean isConvex(double angle) {
        return angle <= 180;
    }

    private int getMaxConvexVertex(Map<Point, Set<Point>> hullCopy,
                                              Point recent,
                                              SortedAdjacent[] sortedAdjacents,
                                              Set<Point> edges) {
        int max = -1;
        if (edges.size() > 0) {
            Set<Point> sortedEdges = new LinkedHashSet<>();
            for (SortedAdjacent sa : sortedAdjacents) {
                sortedEdges.add(sa.point);
            }
            hullCopy.put(recent, sortedEdges);
            edges = sortedEdges;

            if (isConvex(sortedAdjacents[0].angle)) {
                max = 0;
                for (int i = 1; i < sortedAdjacents.length; i++) {
                    if (!isConvex(sortedAdjacents[i].angle)) {
                        break;
                    }
                    if (sortedAdjacents[max].angle <= sortedAdjacents[i].angle) {
                        max = i;
                    }
                }
            }
        }
        return max;
    }

    private void addVertexToTriangulation(Map<Point, Set<Point>> hull,
                                          Point recent,
                                          SortedAdjacent max,
                                          Set<Point> edges,
                                          List<Point> triangulation,
                                          Set<Point> pointsInTriangulation) {
        // When a vertex is added to triangulation, it should be removed from the hull copy.
        edges.remove(max.point);
        hull.get(max.point).remove(recent);
        // This means that the vertex will not be accessible from any of its neighbors.
        // However, the neighbors will be accessible for the vertex to find the next largest convex adjacent vertex.
        for (Point p : hull.get(max.point)) {
            hull.get(p).remove(max.point);
        }
        // Now, add the point to the triangulation and mark is as "added to triangulation".
        triangulation.add(max.point);
        pointsInTriangulation.add(max.point);
    }



    private void advance(Map<Point, Set<Point>> topHull,
                                    Map<Point, Set<Point>> bottomHull,
                                    List<Point> triangulation) throws Exception {
        if (triangulation == null || triangulation.size() < 3) {
            throw new Exception("Initial triangulation should contain one initial face.");
        }

        // make a copy of the top and bottom hulls...
        Map<Point, Set<Point>> top = ConvexHullUtils.deepCopyHull(topHull);
        Map<Point, Set<Point>> bottom = ConvexHullUtils.deepCopyHull(bottomHull);

        // initialize three pointers that act as iterator and wraps around between the two hulls.
        Set<Point> pointsInTriangulation = new LinkedHashSet<>(triangulation);
        Point old = triangulation.get(0);
        Point recentTop = triangulation.get(1);
        Point recentBottom = triangulation.get(2);
        Set<Point> adjacentSorted = new HashSet<>();
        while(true) {
            // Type 1 comparisons
            /* Processing top hull and finding the next possible point from top hull for triangulating... */
            Set<Point> incidentEdgesTop = top.getOrDefault(recentTop, new LinkedHashSet<>());
            removePointsInTriangulation(top, recentTop, pointsInTriangulation);
            SortedAdjacent[] sortedAdjacentsTop = getSortedAdjacents(recentTop, recentBottom, old, incidentEdgesTop);

            int maxTopIdx = getMaxConvexVertex(top, recentTop, sortedAdjacentsTop, incidentEdgesTop);
            SortedAdjacent maxTop = null;
            if (maxTopIdx >= 0) {
                maxTop = sortedAdjacentsTop[maxTopIdx];
            }

            /* Processing bottom hull and finding the next possible point from bottom hull for triangulating... */
            Set<Point> incidentEdgesBottom = bottom.getOrDefault(recentBottom, new LinkedHashSet<>());
            removePointsInTriangulation(bottom, recentBottom, pointsInTriangulation);
            SortedAdjacent[] sortedAdjacentsBottom = getSortedAdjacents(recentTop, recentBottom, old, incidentEdgesBottom);

            int maxBottomIdx = getMaxConvexVertex(bottom, recentBottom, sortedAdjacentsBottom, incidentEdgesBottom);
            SortedAdjacent maxBottom = null;
            if (maxBottomIdx >=0) {
                maxBottom = sortedAdjacentsBottom[maxBottomIdx];
            }

            if (maxBottom == null && maxTop == null) {
                break;
            }

            // Type 2 comparison...
            if ((maxTop == null) || (maxBottom != null && (maxBottom.angle > maxTop.angle))) {
                maxBottom.point.isBelongsToUpperHalf = false;
                addVertexToTriangulation(bottom, recentBottom, maxBottom, incidentEdgesBottom, triangulation, pointsInTriangulation);
                removeUntilMaxConvexVertex(bottom, recentBottom, sortedAdjacentsBottom, incidentEdgesBottom);
                old = recentBottom;
                recentBottom = maxBottom.point;
            } else if ((maxBottom == null) || (maxTop != null && (maxBottom.angle <= maxTop.angle))) {
                maxTop.point.isBelongsToUpperHalf = true;
                addVertexToTriangulation(top, recentTop, maxTop, incidentEdgesTop, triangulation, pointsInTriangulation);
                removeUntilMaxConvexVertex(top, recentTop, sortedAdjacentsTop, incidentEdgesTop);
                old = recentTop;
                recentTop = maxTop.point;
            }
        }
    }


    private List<Point> triangulate(Map<Point, Set<Point>> top, Map<Point, Set<Point>> bottom) throws Exception {
        // Theoretically, this method should run in O(p+q).
        Graham2D projector = new Graham2D();

        Point[] topPoints = new Point[top.keySet().size()];
        top.keySet().toArray(topPoints);
        Point[] top2D = projector.convexHull(topPoints);

        Point[] bottomPoints = new Point[bottom.keySet().size()];
        bottom.keySet().toArray(bottomPoints);
        projector.convexHull(bottomPoints);
        Point[] bottom2D = projector.convexHull(bottomPoints);

        // Step 1: Find the initial tangent between the hulls.
        Tangent rightTangent = getRightTangent(top2D, bottom2D); // O(p+q)

        // Step 2: Wrap around between the hulls and form a cylindrical triangulation.
        List<Point> triangulation = new LinkedList<>();
        Point projectedPoint = new Point(rightTangent.one.x, rightTangent.one.y, Math.min(rightTangent.one.z, rightTangent.other.z)-1);
        triangulation.add(projectedPoint); // add a dummy point to the triangulation.
        rightTangent.one.isBelongsToUpperHalf = true;
        triangulation.add(rightTangent.one); // add the point of the tangent from upper hull.
        rightTangent.other.isBelongsToUpperHalf = false;
        triangulation.add(rightTangent.other); // add the point of the tangent from lower hull.
        advance(top, bottom, triangulation); // use gift-wrapping kind of algorithm to wrap around the triangulation between the hulls.
        return triangulation;
    }

    private Map<Point, Set<Point>> joinCH(Map<Point, Set<Point>> top, Map<Point, Set<Point>> bottom, List<Point> triangulation) {
        Map<Point, Set<Point>> hull = new HashMap<>();
        // Join the two convex hulls into a single convex hull.
        for (Map.Entry<Point, Set<Point>> entry : top.entrySet()) {
            hull.put(entry.getKey(), entry.getValue());
        }

        for (Map.Entry<Point, Set<Point>> entry : bottom.entrySet()) {
            hull.put(entry.getKey(), entry.getValue());
        }

        Point old = triangulation.get(0);
        Point recentTop = triangulation.get(1);
        Point recentBottom = triangulation.get(2);
        for (int i = 3 ; i < triangulation.size() ; i++) {
            Point next = triangulation.get(i);
            double angle = ConvexHullUtils.getAngleBetweenPlanes(recentTop, recentBottom, old, next, false);

            if (next.isBelongsToUpperHalf) {
                Set<Point> edges = new LinkedHashSet<>(hull.getOrDefault(recentTop, new LinkedHashSet<>()));
                for (Point p : edges) {
                    double newAngle = ConvexHullUtils.getAngleBetweenPlanes(recentTop, recentBottom, old, p, false);
                    if (newAngle < angle) {
                        for (Point edge: hull.get(p)) {
                            hull.getOrDefault(edge, new LinkedHashSet<>()).remove(p);
                        }
                        hull.getOrDefault(p, new LinkedHashSet<>()).clear();
                    }
                }
                old = recentTop;
                recentTop = next;
            } else {
                Set<Point> edges = new LinkedHashSet<>(hull.getOrDefault(recentBottom, new LinkedHashSet<>()));
                for (Point p : edges) {
                    double newAngle = ConvexHullUtils.getAngleBetweenPlanes(recentTop, recentBottom, old, p, false);
                    if (newAngle < angle) {
                        for (Point edge: hull.get(p)) {
                            hull.getOrDefault(edge, new LinkedHashSet<>()).remove(p);
                        }
                        hull.getOrDefault(p, new LinkedHashSet<>()).clear();
                    }
                }
                old = recentBottom;
                recentBottom = next;
            }
        }
        triangulation.remove(0);
        // Use the triangulation and add edges that connect the two hulls together.
        // Imagine a person climbing a mountain. We have two pointers that act as two hands.
        // As we move the two pointers, we create edges between hulls.
        Point lastSeenTopPoint = triangulation.get(0), lastSeenBottomPoint = triangulation.get(1);
        Set<Point> edges = hull.getOrDefault(lastSeenBottomPoint, new LinkedHashSet<>());
        edges.add(lastSeenTopPoint);
        hull.put(lastSeenBottomPoint, edges);
        edges = hull.getOrDefault(lastSeenTopPoint, new LinkedHashSet<>());
        edges.add(lastSeenBottomPoint);
        hull.put(lastSeenTopPoint, edges);
        for (int i = 2 ; i < triangulation.size() ; i++) {
            Point curr = triangulation.get(i);
            if (curr.isBelongsToUpperHalf) {
                // intra hull edges are already present.
                lastSeenTopPoint = curr;
                edges = hull.getOrDefault(curr, new LinkedHashSet<>());
                edges.add(lastSeenBottomPoint);
                hull.put(curr, edges);
                edges = hull.getOrDefault(lastSeenBottomPoint, new LinkedHashSet<>());
                edges.add(curr);
                hull.put(lastSeenBottomPoint, edges);
            }
            else {
                // intra hull edges are already present.
                lastSeenBottomPoint = curr;
                edges = hull.getOrDefault(curr, new LinkedHashSet<>());
                edges.add(lastSeenTopPoint);
                hull.put(curr, edges);
                edges = hull.getOrDefault(lastSeenTopPoint, new LinkedHashSet<>());
                edges.add(curr);
                hull.put(lastSeenTopPoint, edges);
            }
        }

        return hull;
    }



    private Map<Point, Set<Point>> merge(Map<Point, Set<Point>> top, Map<Point, Set<Point>> bottom) throws Exception {
        return joinCH(top, bottom, triangulate(top, bottom));
    }

    private Map<Point, Set<Point>> convexHullUtil(Point[] vertices, int start, int end) throws Exception {
        if (end - start <= 4) {
            // Base case: If there are four vertices, it forms a tetrahedron. So convex hull has four faces.
            Map<Point, Set<Point>> result = new HashMap<>();
            for (int i = start ; i <=end ; i++) {
                Set<Point> e = new LinkedHashSet<>();
                for (int j = start ; j <= end ; j++) {
                    if (i != j) {
                        e.add(vertices[j]);
                    }
                }
                result.put(vertices[i],e);
            }
            return result;
        }

        int mid = start + (end-start)/2; // find mid point for split.
        return merge(convexHullUtil(vertices, start, mid), convexHullUtil(vertices, mid+1, end));
    }

    Map<Point, Set<Point>> convexHull(Set<Point> polyhedron) throws Exception {
        if (polyhedron == null || polyhedron.isEmpty()) {
            return new HashMap<>();
        }

        // sort the points by y-coord
        Point[] vertices = new Point[polyhedron.size()];
        polyhedron.toArray(vertices);
        Arrays.sort(vertices, (o1, o2) -> (o1.y.equals(o2.y)) ? 0 : ((o1.y > o2.y) ? -1 : 1)); // O(nlogn)
        return convexHullUtil(vertices, 0, vertices.length-1); // O(nlogn), theoretically.
    }
}
