def delay_advance_signal(signal, k):

    if k > 0:
        # Advance the signal by k steps
        result = [0] * k + signal[:-k]
    elif k < 0:
        # Delay the signal by |k| steps
        result = signal[-k:] + [0] * abs(k)
    else:
        # No delay or advance
        result = signal

    return result


# Example usage:
original_signal = [1, 2, 3, 4, 5]
k_steps = 2
delayed_signal = delay_advance_signal(original_signal, k_steps)

print(f"Original Signal: {original_signal}")
print(f"Delayed/Advanced Signal by {k_steps} steps: {delayed_signal}")
