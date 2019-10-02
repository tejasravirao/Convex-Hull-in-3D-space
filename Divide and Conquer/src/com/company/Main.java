package com.company;

import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        /*
         * This program requires one command line argument that indicates the absolute path to the output file.
         * The program will ask for input file path.
         */
        BufferedReader inputReader = new BufferedReader(new InputStreamReader(System.in));
        System.out.print("Absolute Path to input file: ");
        String inputFileName = inputReader.readLine();
        inputReader.close();
        inputReader = new BufferedReader(new FileReader(new File(inputFileName)));
        Set<Point> points = new LinkedHashSet<>();
        String line;
        while((line = inputReader.readLine()) != null) {
            String[] point = line.split(",");
            points.add(new Point(Double.parseDouble(point[0].trim()), Double.parseDouble(point[1].trim()), Double.parseDouble(point[2].trim())));
        }


        Preparata preparata = new Preparata();

        Map<Point, Set<Point>> hull = preparata.convexHull(points); // doesn't work with collinear points. requires general positioning.

        BufferedWriter bw = new BufferedWriter(new FileWriter(new File(args[0])));
        for (Map.Entry<Point, Set<Point>> entry : hull.entrySet()) {
            for (Point p : entry.getValue()) {
                bw.write(entry.getKey().x + "," + entry.getKey().y + "," + entry.getKey().z + "\t" + p.x + "," + p.y + "," + p.z + "\n");
                System.out.println(entry.getKey() + " - " + p);
            }
        }

        bw.close();

    }
}
