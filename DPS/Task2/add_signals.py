class Add_Signals:
    def __init__(self):
        pass

    def validate_points(self, points):
        if not isinstance(points, list) or not all(isinstance(p, list) and len(p) == 2 for p in points):
            raise ValueError("Invalid input format. Expected a list of (x, y) pairs.")
        return True

    def adding(self, points1, points2):
        if not (self.validate_points(points1) and self.validate_points(points2)):
            return  # Validation failed
        if len(points1) != len(points2):
            raise ValueError("Length of points1 is not equal to points2")
        for i in range(len(points1)):
            points1[i][1] += points2[i][1]
        return points1

    def subtracting(self, points1, points2):
        if not (self.validate_points(points1) and self.validate_points(points2)):
            return  # Validation failed
        if len(points1) != len(points2):
            raise ValueError("Length of points1 is not equal to points2")
        for i in range(len(points1)):
            points1[i][1] -= points2[i][1]
        return points1
