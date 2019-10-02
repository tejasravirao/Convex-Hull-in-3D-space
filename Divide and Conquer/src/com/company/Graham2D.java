package com.company;
import com.company.Preparata.*;

import java.util.Arrays;
import java.util.Comparator;
import java.util.Stack;

public class Graham2D {

//    https://www.geeksforgeeks.org/convex-hull-set-2-graham-scan/

    Point nextToTop(Stack<Point> stack) {
        Point p = stack.peek();
        stack.pop();
        Point res = stack.peek();
        stack.push(p);
        return res;
    }

    void swap(Point[] points, int one, int other) {
        Point temp = points[one];
        points[one] = points[other];
        points[other] = temp;
    }

    double distSquare(Point p1, Point p2) {
        return (p1.x - p2.x)*(p1.x - p2.x) +
                (p1.y - p2.y)*(p1.y - p2.y);
    }

    int orientation(Point p, Point q, Point r) {
        double val = (q.y - p.y) * (r.x - q.x) -
                (q.x - p.x) * (r.y - q.y);

        if (val == 0.0) return 0;
        return (val > 0.0)? 1: 2;
    }

    Point[] convexHull(Point[] originalPoints) {
        Point p0;
        Point[] points = new Point[originalPoints.length];
        System.arraycopy(originalPoints, 0, points, 0 , originalPoints.length);
        int n = points.length;
        int min = 0;
        double ymin = points[0].y;
        for (int i = 1; i < n; i++)
        {
            double y = points[i].y;

            if ((y < ymin) || (ymin == y &&
                    points[i].x < points[min].x)) {
                ymin = points[i].y;
                min = i;
            }
        }

        swap(points,0, min);

        p0 = points[0];
        Arrays.sort(points, 1, points.length, new Comparator<Point>() {
            @Override
            public int compare(Point o1, Point o2) {
                Point p1 = o1;
                Point p2 = o2;

                // Find orientation
                int o = orientation(p0, p1, p2);
                if (o == 0)
                    return (distSquare(p0, p2) >= distSquare(p0, p1))? -1 : 1;

                return (o == 2)? -1: 1;
            }
        });
        
        int m = 1; 
        for (int i=1; i<n; i++) {
            while (i < n-1 && orientation(p0, points[i],
                    points[i+1]) == 0) {
                i++;
            }
            points[m] = points[i];
            m++;
        }

        if (m < 3) {
            return new Point[0];
        }

        Stack<Point> result = new Stack<>();
        result.push(points[0]);
        result.push(points[1]);
        result.push(points[2]);
        for (int i = 3; i < m; i++) {
            while (orientation(nextToTop(result), result.peek(), points[i]) != 2) {
                result.pop();
            }
            result.push(points[i]);
        }

        Point[] resultArr = new Point[result.size()];
        int i = 0;
        while (!result.isEmpty()) {
            resultArr[i++] = result.pop();
        }

        return resultArr; // O(nlogn) because of the sorting.
    }
}
