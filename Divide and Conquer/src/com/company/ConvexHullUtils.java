package com.company;

import java.util.*;

public class ConvexHullUtils {

    static double[] crossProduct(double[] vectorOne, double[] vectorTwo) {
        return new double[]{
                vectorOne[1]*vectorTwo[2] - vectorOne[2]*vectorTwo[1],
                vectorOne[2]*vectorTwo[0] - vectorOne[0]*vectorTwo[2],
                vectorOne[0]*vectorTwo[1] - vectorOne[1]*vectorTwo[0]
        };
    }



    static double dotProduct(double[] vectorOne, double[] vectorTwo) {
        return (vectorOne[0]*vectorTwo[0]) + (vectorOne[1]*vectorTwo[1]) + (vectorOne[2]*vectorTwo[2]);
    }



    static double slope(Point one, Point other) {
        if (one == null || other == null) {
            return 0;
        }

        return ((other.y - one.y) / (other.x - one.x));
    }


    static Map<Point, Set<Point>> deepCopyHull(Map<Point, Set<Point>> hull) {
        if (hull == null ) {
            return null;
        }
        if (hull.isEmpty()) {
            return new HashMap<>();
        }
        Map<Point, Set<Point>> result = new HashMap<>();
        for (Map.Entry<Point, Set<Point>> entry : hull.entrySet()) {
            Set<Point> edgeCopy = new LinkedHashSet<>(entry.getValue());
            result.put(entry.getKey(), edgeCopy);
        }
        return result;
    }
    static double getAngle(Point pivot, Point axisEnd, Point current, Point next, boolean isCounterClockwise) {
        double[] s = new double[]{pivot.x - axisEnd.x, pivot.y - axisEnd.y, pivot.z - axisEnd.z};
        double[] r = new double[]{current.x - axisEnd.x, current.y - axisEnd.y, current.z - axisEnd.z};
        double[] t = new double[]{next.x - pivot.x, next.y - pivot.y, next.z - pivot.z};

//         double sMagnitude = Math.sqrt(Math.pow(s[0],2)+Math.pow(s[1],2)+Math.pow(s[2],2));
        double[] rsCross = ConvexHullUtils.crossProduct(r,s);
        double cotx = (-1 * ConvexHullUtils.dotProduct(t, ConvexHullUtils.crossProduct(rsCross, s)) / (ConvexHullUtils.dotProduct(t, rsCross)));
        return cotx;
    }

    static double getAngleBetweenPlanes(Point pivot, Point axisEnd, Point current, Point next, boolean isCounterClockwise) {
        double[] axis = new double[]{pivot.x - axisEnd.x, pivot.y - axisEnd.y, pivot.z - axisEnd.z};
        double[] currentVector = new double[]{current.x - pivot.x, current.y - pivot.y, current.z - pivot.z};
        double[] nextVector = new double[]{next.x - pivot.x, next.y - pivot.y, next.z - pivot.z};

        double[] referencePlane = ConvexHullUtils.crossProduct(axis, currentVector);
        double[] nextPlane = ConvexHullUtils.crossProduct(axis, nextVector);

        if (ConvexHullUtils.getMagnitude(nextPlane) == 0) {
//             If the magnitude of nextPlane is 0, it means that the axis and newVector are collinear. If they're parallel
//             return 180. Else if they're anti-parallel return 360.
            return 180;
        }

        double cosine_angle = ConvexHullUtils.dotProduct(referencePlane, nextPlane)/(ConvexHullUtils.getMagnitude(referencePlane) * ConvexHullUtils.getMagnitude(nextPlane));
        double angle = Math.toDegrees(Math.acos(cosine_angle));
        angle = cosine_angle < 0 ? (360-angle) : angle;
        return (isCounterClockwise) ? (360-angle) : angle;
    }

    static double getMagnitude(double[] vector) {
         return Math.sqrt(Math.pow(vector[0],2)+Math.pow(vector[1],2)+Math.pow(vector[2],2));
    }

    static int findMaxIdx(Point[] polygon) {
        if (polygon == null || polygon.length == 0) {
            return -1;
        }

        int iter = 0;
        int maxIdx = iter;
        do {
            if (polygon[iter].x > polygon[maxIdx].x) {
                maxIdx = iter;
            }
            iter = (iter+1) % polygon.length;
        } while(iter != 0);
        return maxIdx;
    }
}
