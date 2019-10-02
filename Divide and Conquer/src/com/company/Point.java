package com.company;

public class Point {
    Double x, y, z;
    boolean isBelongsToUpperHalf;

    Point() {}

    Point(Double x, Double y, Double z) {
        this.x = x;
        this.y = y;
        this.z = z;
    }

    @Override
    public boolean equals(Object o) {
        if (o instanceof Point) {
            Point other = (Point) o;
            return this.x.doubleValue() == other.x.doubleValue() && this.y.doubleValue() == other.y.doubleValue() && this.z.doubleValue() == other.z.doubleValue();
        }
        return false;
    }

    @Override
    public int hashCode() {
        int result = 0;
        if (x != null) {
            result += x.hashCode();
        }
        if (y != null) {
            result += y.hashCode();
        }
        if (z != null) {
            result += z.hashCode();
        }
        return result;
    }

    public String toString() {
        return "("+x.toString()+", "+y.toString()+", "+z.toString()+")";
    }
}
