

def file_read():
    file = open("data.txt", 'r')

    if file.closed:
        print("File not opened")

    points = []
    for line in file.readlines():
        points.append([int(x) for x in line.split(',')])

    return points
