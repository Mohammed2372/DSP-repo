class Add_Signals:
    multiplication_constant = None
    shift_constant = None
    norm_mode = None

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

    def multiplication(self, points1):  # multiplcating the y's in points with constant
        if not (self.validate_points(points1)):
            return
        for i in range(len(points1)):
            points1[i][1] *= self.multiplication_constant
        return points1

    def squaring(self, points1):  # squaring every y int points
        if not (self.validate_points(points1)):
            return  # Validation failed
        for i in range(len(points1)):
            points1[i][1] *= points1[i][1]
        return points1

    def shift(self, points1):  # shift the y's in points with constant
        if not (self.validate_points(points1)):
            return
        for i in range(len(points1)):
            points1[i][0] -= self.shift_constant
        return points1

    def norm(self, points1):  # shift the y's in points with constant

        y = [pair[1] for pair in points1]
        x = [pair[0] for pair in points1]

        if self.norm_mode == "-1 to 1":
            min_value = min(y)
            max_value = max(y)
            normalized_data = [(2 * (x - min_value) / (max_value - min_value)) - 1 for x in y]
            y = normalized_data
        elif self.norm_mode == "0 to 1":
            min_value = min(y)
            max_value = max(y)
            normalized_data = [(x - min_value) / (max_value - min_value) for x in y]
            y = normalized_data

        merged_array = [(x, y) for x, y in zip(x, y)]
        return merged_array

    def acc(self, points1):  # shift the y's in points with constant

        y = [pair[1] for pair in points1]
        x = [pair[0] for pair in points1]

        for i in range(1, len(y)):
            y[i] += y[i - 1]

        merged_array = [(x, y) for x, y in zip(x, y)]
        print(merged_array)
        return merged_array
