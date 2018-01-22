def generate_table(n_rows, m_cols, repeated_times, random_max):
    import random
    data = list()
    x = 0
    while x * repeated_times <= n_rows:
        for t in range(0, repeated_times):
            l = list()
            l.append(x)
            for j in range(0, m_cols):
                l.append(random.randint(1, random_max))
            data.append(l)
        x = x + 1
    return data


