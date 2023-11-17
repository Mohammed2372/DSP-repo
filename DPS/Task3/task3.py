class quantization:
    global x, y, ranges, index, quant, incoded, error, selectedValue
    x = []
    y = []
    ranges = []
    index = []
    quant = []
    incoded = []
    error = []

    def __init__(self):
        pass

    def set_x_y(self, points):
        self.x = [item[0] for item in points]
        self.y = [item[1] for item in points]

    def bits(self):
        max_value = max(y)
        min_value = min(y)
        n = entry_var.get()
        levels = pow(2, n)
        lamda = (max_value - min_value) / levels
        for i in range(levels):
            midPoint = (min_value + (min_value + lamda)) / 2
            Range = [round(min_value, 3), round((min_value + lamda), 3),
                     round(midPoint, 3), i + 1]
            ranges.append(Range)
            min_value += lamda
        for i in y:
            for j in ranges:
                if i >= j[0]:
                    if i <= j[1]:
                        quan.append(j[2])
                        index.append(j[3])
                        break
        for i in range(len(y)):
            error.append(round(quan[i] - y[i], 3))
        for i in index:
            binary_representation = format(i - 1, f'0{n}b')
            incoded.append(binary_representation)
        print(incoded)
        print(quan)

    def levels(self):
        max_value = max(y)
        min_value = min(y)
        levels = entry_var.get()
        lamda = (max_value - min_value) / levels
        for i in range(levels):
            midPoint = (min_value + (min_value + lamda)) / 2
            Range = [round(min_value, 3), round((min_value + lamda), 3),
                     round(midPoint, 3), i + 1]
            ranges.append(Range)
            min_value += lamda
        for i in y:
            for j in ranges:
                if i >= j[0]:
                    if i <= j[1]:
                        quan.append(j[2])
                        index.append(j[3])
        for i in range(len(y)):
            error.append(round(quan[i] - y[i], 3))
        for i in index:
            num_digits = math.ceil(math.log(levels, 2))
            binary_representation = format(
                i - 1, f'0{num_digits}b')
            incoded.append(binary_representation)
        print(index)
        print(incoded)
        print(quan)
        print(error)

    def calculate_bits(self, points, selectedValue):
        self.set_x_y(points)
        if selectedValue == "bits":
            self.bits()
        else:
            self.levels()
