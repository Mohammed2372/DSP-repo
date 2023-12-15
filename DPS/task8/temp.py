def fast_correlatoin(frame):
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    new_window = tk.Toplevel(frame)
    new_window.geometry("200x300")
    FastFrame = tk.Frame(new_window)
    uploadButton1 = tk.Button(
        FastFrame, text="upload signal", command=lambda: read_data(x1, y1))
    uploadButton2 = tk.Button(
        FastFrame, text="upload signal", command=lambda: read_data(x2, y2))

    len1 = len(y1)
    len2 = len(y2)

    if len1 < len2:
        y1 += [0] * (len2 - len1)
    elif len1 > len2:
        y2 += [0] * (len1 - len2)

    def calc_fast_correlation():
        nonlocal y1, y2
        out1 = []
        out2 = []
        DFT(y1, out1)
        DFT(y2, out2)
        x1 = out1
        x2 = out2
        x3 = []
        for i in x1:
            i = complex(i.real, i.imag * -1)
        for i in range(len(x1)):
            x3.append(x1[i]*x2[i])
        # IDFT
        result = []
        for i in range(len(x3)):
            k = i
            sum = 0
            for y in range(len(x3)):
                sum += x3[y] * \
                    cmath.exp((1j * 2*math.radians(180)*k*y)/len(x3))
                if abs(sum.imag) < tolerance:
                    sum = complex(sum.real, 0)
                R = sum.real
                I = sum.imag
                R = round(sum.real, 0)
                I = round(sum.imag, 0)
            result.append(round(sum.real, 0)/len(x3))
            sum = 0
        for i in range(len(result)):
            # print(result[i])
            result[i] = result[i] / len(result)
            print(result[i])
        with open("fastCorelation.txt", "w") as myFile:
            for i in range(len(result)):
                myFile.write(str(i) + ' ' +
                             str(result[len(result) - i - 1]) + "\n")

    calcBtn = tk.Button(FastFrame, text="calc",
                        command=lambda: calc_fast_correlation())
    uploadButton1.pack(pady=10)
    uploadButton2.pack(pady=10)
    calcBtn.pack(pady=10)
    FastFrame.pack()


def fast_convolution(frame):
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    new_window = tk.Toplevel(frame)
    new_window.geometry("200x300")
    FastFrame = tk.Frame(new_window)
    uploadButton1 = tk.Button(
        FastFrame, text="upload signal", command=lambda: read_data(x1, y1))
    uploadButton2 = tk.Button(
        FastFrame, text="upload signal", command=lambda: read_data(x2, y2))
    len1 = len(y1)
    len2 = len(y2)

    if len1 < len2:
        y1 += [0] * (len2 - len1)
    elif len1 > len2:
        y2 += [0] * (len1 - len2)

    def calc_fast_convolution():
        nonlocal y1, y2
        out1 = []
        out2 = []
        DFT(y1, out1)
        DFT(y2, out2)
        x1 = out1
        x2 = out2
        x3 = []
        for i in range(len(x1)):
            x3.append(x1[i]*x2[i])
        # IDFT
        result = []
        for i in range(len(x3)):
            k = i
            sum = 0
            for y in range(len(x3)):
                sum += x3[y] * \
                    cmath.exp((1j * 2*math.radians(180)*k*y)/len(x3))
                if abs(sum.imag) < tolerance:
                    sum = complex(sum.real, 0)
                R = sum.real
                I = sum.imag
                R = round(sum.real, 0)
                I = round(sum.imag, 0)
            result.append(round(sum.real, 0)/len(x3))
            sum = 0
        with open("fastConvolution.txt", "w") as myFile:
            for i in range(len(result)):
                myFile.write(str(i) + ' ' +
                             str(result[len(result) - i - 1]) + "\n")

    calcBtn = tk.Button(FastFrame, text="calc",
                        command=lambda: calc_fast_convolution())
    uploadButton1.pack(pady=10)
    uploadButton2.pack(pady=10)
    calcBtn.pack(pady=10)
    FastFrame.pack()