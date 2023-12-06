def calculate_max_distance(race_len):
    return int((race_len/2) ** 2)

def part_1(times, thresholds):
    mult = 1
    for i in range(len(times)):
        mult *= calculate_num_ways_to_win(times[i], thresholds[i])
    return mult

def part_2(race_time, thresholds):
    return calculate_num_ways_to_win(race_time, threshold)


def generate_series(n):
    series = []
    num = 1 - (n % 2)

    while len(series) < n:
        series.extend([num] * num)
        num += 2  # Increment by 2 for odd numbers in the series

    return series

def calculate_distances(race_len):
    race_distances = []
    for windup in range(race_len+1):
        race_distances.append((windup,windup * (race_len - windup)))
    return race_distances


def calculate_num_ways_to_win(race_len, threshold):
    max_threshold_for_victory = calculate_max_distance(race_len) - 1
    num_ways_to_win = 1 + ((race_len) % 2)

    while max_threshold_for_victory > threshold:
        num_ways_to_win += 2
        threshold += num_ways_to_win
    return num_ways_to_win

def test_part_1():
    times = [7,15,30]
    thresholds = [9,40,200]
    print(part_1(times, thresholds))
    assert part_1(times, thresholds) == 288

if __name__ == '__main__':
    test_part_1()
    times = [58,99,64,69]
    thresholds = [478,2232,1019,1071]
    print(part_1(times, thresholds))

    race_time = 58996469
    threshold = 478223210191071
    print(part_2(race_time, threshold))

    # threshold = 190
    # race_len = 28
    # distances = calculate_distances(race_len)
    # print(distances)
    # for i in range(calculate_max_distance(race_len)):
    #     wins = 0
    #     for j in distances:
    #         if i < j[1]:
    #             wins +=1
    #     print("threshold:", i, "wins:", wins)

    # print(calculate_num_ways_to_win(race_len, threshold))