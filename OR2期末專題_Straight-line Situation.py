import math
from geopy.distance import geodesic

def create_data_model():
    data = {}
    data['locations'] = [
        (25.077293073350997, 121.43690044581943),  # 風驊
        (24.157826638346272, 120.72227093813007),  # 中X
        (25.058109202430217, 121.53854330628305),  # 新X
        (25.06746555211543, 121.51341769582824),   # 廣X
        (24.985403373655494, 121.25621589582572),  # 來X福
        (23.01288710430495, 120.22802419577067)    # 一流台南店
    ]
    data['num_locations'] = len(data['locations'])
    return data

def compute_distance(location1, location2):
    return geodesic(location1, location2).kilometers


def tsp_dp():
    data = create_data_model()
    num_locations = data['num_locations']
    locations = data['locations']

    # 初始化動態規劃表格
    dp = [[math.inf] * num_locations for _ in range(2**num_locations)]

    # 設置起點和終點的狀態
    start_state = 1  # 二進制表示為"000001"
    end_state = 2**num_locations - 1  # 二進制表示為全1

    # 初始化起點到各個城市的距離
    for i in range(num_locations):
        dp[1 << i][i] = compute_distance(locations[0], locations[i])

    # 遍歷所有子集狀態
    for state in range(start_state, end_state + 1):
        for dest in range(num_locations):
            if state & (1 << dest):  # 確保目的地在當前子集中
                prev_state = state & ~(1 << dest)  # 移除目的地的狀態
                for prev_dest in range(num_locations):
                    if prev_state & (1 << prev_dest):  # 確保前一個目的地在前一個子集中
                        dp[state][dest] = min(dp[state][dest], dp[prev_state][prev_dest] + compute_distance(locations[prev_dest], locations[dest]))

    # 找到最短路徑的總距離
    min_distance = math.inf
    last_dest = 0  # 設置初始值為起點
    for dest in range(1, num_locations):
        distance = dp[end_state][dest] + compute_distance(locations[dest], locations[0])
        if distance < min_distance:
            min_distance = distance
            last_dest = dest

    # 從動態規劃表格中重建最短路徑
    path = [0]
    state = end_state
    dest = last_dest
    total_distance = 0  # 增加變數來計算最短路徑的總距離
    while state != start_state:
        path.append(dest)
        prev_state = state & ~(1 << dest)
        next_dest = -1  # 初始化下一個目的地
        for i in range(num_locations):
            if prev_state & (1 << i) and dp[prev_state][i] + compute_distance(locations[i], locations[dest]) == dp[state][dest]:
                next_dest = i  # 更新下一個目的地
                break
        total_distance += compute_distance(locations[dest], locations[next_dest])  # 增加計算距離
        dest = next_dest
        state = prev_state

    # 添加最後一個城市回到起點
    path.append(0)
    total_distance += compute_distance(locations[path[-2]], locations[0])  # 增加計算距離

    # 輸出結果
    city_names = ['風驊', '中X', '新X', '廣X', '來X福', '一流台南店']
    print("最短路徑:")
    for i in range(len(path) - 1):
      print(city_names[path[i]], end=' -> ')
    print(city_names[path[-1]])
    print("最短距離:", total_distance)

# 解決TSP問題
tsp_dp()