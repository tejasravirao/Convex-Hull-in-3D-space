package com.company;

class Tangent {
    Point one, other;

    Tangent() {}

    Tangent(Point one, Point other) {
        this.one = one;
        this.other = other;
    }

    public String toString() {
        return one.toString()+" - " + other.toString();
    }
}
