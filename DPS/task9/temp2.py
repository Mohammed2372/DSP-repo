def task10_frame_window():
    new_window = tk.Toplevel(root)
    new_window.geometry("200x700")
    frame10 = tk.Frame(new_window)
    minF = tk.IntVar(frame10)
    maxF = tk.IntVar(frame10)
    Fs = tk.IntVar(frame10)
    newFs = tk.IntVar(frame10)

    minFLabel = tk.Label(frame10, text="minF")
    maxFLabel = tk.Label(frame10, text="maxF")
    fsLabel = tk.Label(frame10, text="FS")
    newfsFLabel = tk.Label(frame10, text="newFS")

    minFEntry = tk.Entry(frame10, textvariable=minF)
    minFLabel.pack(pady=5)
    minFEntry.pack(pady=5)
    maxFEntry = tk.Entry(frame10, textvariable=maxF)
    maxFLabel.pack(pady=5)
    maxFEntry.pack(pady=5)
    fsEntry = tk.Entry(frame10, textvariable=Fs)
    fsLabel.pack(pady=5)
    fsEntry.pack(pady=5)
    newfsEntry = tk.Entry(frame10, textvariable=newFs)
    newfsFLabel.pack(pady=5)
    newfsEntry.pack(pady=5)
    filterd = []
    filterdA = []
    filterdB = []
    test = []
    filter = []
    filterA = []
    filterB = []
    correlation = []
    correlationA = []
    correlationB = []
    DCT = []
    DCT_A = []
    DCT_B = []
    newCor = []
    newCorA = []
    newCorB = []
    uploadButton1 = tk.Button(
        frame10, text="upload signal", command=lambda: read_data_new(test))
    uploadButton1.pack(pady=5)

    uploadA = tk.Button(
        frame10, text="upload A", command=lambda: read_data2(listA, "A"))
    uploadA.pack(pady=5)

    uploadB = tk.Button(
        frame10, text="upload B", command=lambda: read_data2(listB, "B"))
    uploadB.pack(pady=5)

    def display_original(y):
        time = np.linspace(0, 100, len(y))
        plt.plot(time, y, label="original ecg")
        plt.legend()
        plt.show()

    def calcClass():
        avg_A = []
        sum_A = 0
        for i in range(len(listA[0])):
            # Calc the avrage
            for j in range(len(listA)):
                sum_A += (listA[j][i]/len(listA))

            # Append in avg list
            avg_A.append(sum_A)
        nonlocal filterdA
        calc("band-pass", Fs.get(), 50, minF.get(),
             maxF.get(), 500, filterA, avg_A, filterdA)
        if newFs.get() / maxF.get() <= 0.5:
            if (newFs.get() > Fs.get()):
                filterdA = upSampling(filterdA, newFs.get() / Fs.get())
            else:
                filterdA = downSampling(filterdA, Fs.get() / newFs.get())
        before = np.array(filterdA)
        after = before - np.mean(before)
        min_value = min(after)
        max_value = max(after)
        normalized_data = [
            (2 * (x - min_value) / (max_value - min_value)) - 1 for x in after]

        sqr_signalA_sum1 = 0
        sqr_signalA_sum2 = 0

        r = 0

        for i in range(len(normalized_data)):

            sqr_signalA_sum1 += normalized_data[i]**2
            sqr_signalA_sum2 += normalized_data[i]**2

        for j in range(len(normalized_data)):
            nonlocal correlationA
            for n in range(len(normalized_data)):
                r += (1/len(normalized_data)) * \
                    (normalized_data[n]*normalized_data[(n+j) %
                     len(normalized_data)])

            correlationA.append(r)
            r = 0
        for i in range(int(len(correlationA)/8)):
            newCorA.append(correlationA[i])
        NDCT = len(newCorA)

        for x in range(NDCT):
            k = 0
            for y in range(NDCT):
                k += newCorA[y] * \
                    math.cos((math.pi / (4 * NDCT)) *
                             (2 * y - 1) * (2 * x - 1))
            k *= math.sqrt(2 / NDCT)
            DCT_A.append(k)
        print(len(DCT_A))

        avg_B = []
        sum_B = 0
        for i in range(len(listB[0])):
            # Calc the avrage
            for j in range(len(listB)):
                sum_B += (listB[j][i]/len(listB))

            # Append in avg list
            avg_B.append(sum_B)

        nonlocal filterdB
        calc("band-pass", Fs.get(), 50, minF.get(),
             maxF.get(), 500, filterB, avg_B, filterdB)
        if newFs.get() / maxF.get() <= 0.5:
            if (newFs.get() > Fs.get()):
                filterdB = upSampling(filterdB, newFs.get() / Fs.get())
            else:
                filterdB = downSampling(filterdB, Fs.get() / newFs.get())
        before = np.array(filterdB)
        after = before - np.mean(before)
        min_value = min(after)
        max_value = max(after)
        normalized_data = [
            (2 * (x - min_value) / (max_value - min_value)) - 1 for x in after]

        sqr_signalA_sum1 = 0
        sqr_signalA_sum2 = 0

        r = 0

        for i in range(len(normalized_data)):

            sqr_signalA_sum1 += normalized_data[i]**2
            sqr_signalA_sum2 += normalized_data[i]**2

        for j in range(len(normalized_data)):
            nonlocal correlationB
            for n in range(len(normalized_data)):
                r += (1/len(normalized_data)) * \
                    (normalized_data[n]*normalized_data[(n+j) %
                     len(normalized_data)])

            correlationB.append(r)
            r = 0
        for i in range(int(len(correlationB)/8)):
            newCorB.append(correlationB[i])
        NDCT = len(newCorB)

        for x in range(NDCT):
            k = 0
            for y in range(NDCT):
                k += newCorB[y] * \
                    math.cos((math.pi / (4 * NDCT)) *
                             (2 * y - 1) * (2 * x - 1))
            k *= math.sqrt(2 / NDCT)
            DCT_B.append(k)

        nonlocal filterd
        calc("band-pass", Fs.get(), 50, minF.get(),
             maxF.get(), 500, filter, test, filterd)
        if newFs.get() / maxF.get() <= 0.5:
            if (newFs.get() > Fs.get()):
                filterd = upSampling(filterd, newFs.get() / Fs.get())
            else:
                filterd = downSampling(filterd, Fs.get() / newFs.get())
        before = np.array(filterd)
        after = before - np.mean(before)
        min_value = min(after)
        max_value = max(after)
        normalized_data = [
            (2 * (x - min_value) / (max_value - min_value)) - 1 for x in after]

        sqr_signalA_sum1 = 0
        sqr_signalA_sum2 = 0

        r = 0

        for i in range(len(normalized_data)):

            sqr_signalA_sum1 += normalized_data[i]**2
            sqr_signalA_sum2 += normalized_data[i]**2

        for j in range(len(normalized_data)):
            nonlocal correlation
            for n in range(len(normalized_data)):
                r += (1/len(normalized_data)) * \
                    (normalized_data[n]*normalized_data[(n+j) %
                     len(normalized_data)])

            correlation.append(r)
            r = 0
        for i in range(int(len(correlation)/8)):
            newCor.append(correlation[i])
        NDCT = len(newCor)

        for x in range(NDCT):
            k = 0
            for y in range(NDCT):
                k += newCor[y] * \
                    math.cos((math.pi / (4 * NDCT)) *
                             (2 * y - 1) * (2 * x - 1))
            k *= math.sqrt(2 / NDCT)
            DCT.append(k)

        corA = calc_correlation(DCT, DCT_A, False)
        corB = calc_correlation(DCT, DCT_B, False)
        countA = 0
        coutnB = 0
    # Classify the test
        for i in range(len(corA)):
            if corA[i] > corB[i]:
                countA += 1
            elif corB[i] > corA[i]:
                coutnB += 1
        if (countA > coutnB):
            print("This signal belongs to class A")
        else:
            print("This signal belongs to class B")


    calcBtnA = tk.Button(frame10, text="calc", command=lambda: calcClass())
    calcBtnA.pack(pady=5)

    plotFilter = tk.Button(frame10, text="plot original",
                           command=lambda: display_original(test))
    plotFilter.pack(pady=5)

    plotCor = tk.Button(frame10, text="plot cor",
                        command=lambda: display_original(correlation))
    plotCor.pack(pady=5)

    plotCor2 = tk.Button(frame10, text="plot cor 2",
                         command=lambda: display_original(newCor))
    plotCor2.pack(pady=5)
    plotDct = tk.Button(frame10, text="plot DCT",
                        command=lambda: display_original(DCT))
    plotDct.pack(pady=5)

    frame10.pack()


# main GUI
root = tk.Tk()
root.geometry("200x600")
root.title("DSP")

# task ten
taskTenBtn = tk.Button(root, text="Task# 9-2", command=task10_frame_window)
taskTenBtn.pack(pady=10)
root.mainloop()