import heapq
from copy import deepcopy

class FindingRoute:

    def __init__(self):
        self.initial_state = None
        self.myCar = None
        self.m = None
        self.n = None
        self.goal_position = None

    # 曼哈頓距離作為啟發函數
    def heuristic(self, state, target):
        for i in range(self.m):
            for j in range(self.n):
                if state[i][j] == self.myCar:  # 找到目標車
                    x, y = i, j
                    return abs(x - target[0]) + abs(y - target[1])
        return float('inf')

    # 找到所有 '  ' 的位置
    def find_empty(self, state):
        empty_positions = []
        for i in range(self.m):
            for j in range(self.n):
                if state[i][j] == ' ':
                    empty_positions.append((i, j))
        return empty_positions

    # 生成所有可能的移動操作
    def get_neighbors(self, state):
        neighbors = []
        empty_positions = self.find_empty(state)

        for empty_x, empty_y in empty_positions:
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 上、下、左、右
            for dx, dy in directions:
                new_x, new_y = empty_x + dx, empty_y + dy
                if 0 <= new_x < self.m and 0 <= new_y < self.n:  # 確保不越界
                    new_state = [row[:] for row in state]  # 深拷貝新的狀態
                    moved_number = new_state[new_x][new_y]  # 記錄被移動的數字
                    new_state[empty_x][empty_y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[empty_x][
                        empty_y]
                    neighbors.append((new_state, moved_number, (dy, dx)))
        return neighbors

    # 判斷目標狀態
    def is_goal(self, state):
        return state[self.goal_position[0]][self.goal_position[1]] == self.myCar  # 目標是 '00' 在 (2, 2) 位置

    # A* 主函數，修改過後會記錄步驟與移動資訊
    def a_star_search(self, initial_state):
        if self.is_goal(initial_state):
            return [(initial_state, None, None)]

        open_list = []
        heapq.heappush(open_list,(0, initial_state, 0, None, None, None))  # (f, state, g, parent, moved_number, direction)
        closed_set = set()
        came_from = {}

        # 確保初始狀態也加入 came_from
        state_tuple = tuple(tuple(row) for row in initial_state)
        came_from[state_tuple] = (None, None, None)

        while open_list:
            _, current_state, g, parent, moved_number, direction = heapq.heappop(open_list)

            state_tuple = tuple(tuple(row) for row in current_state)
            if state_tuple in closed_set:
                continue
            closed_set.add(state_tuple)

            # 記錄來自哪個狀態
            came_from[state_tuple] = (parent, moved_number, direction)

            if self.is_goal(current_state):
                path = []
                while current_state is not None:
                    state_tuple = tuple(tuple(row) for row in current_state)
                    parent, moved_number, direction = came_from.get(state_tuple, (None, None, None))

                    path.append((current_state, moved_number, direction))

                    # 停止回溯的條件
                    if parent is None:
                        break
                    current_state = parent

                path.reverse()
                return path

            for neighbor, moved_number, direction in self.get_neighbors(current_state):
                h = self.heuristic(neighbor, self.goal_position)
                f = g + 1 + h
                neighbor_tuple = tuple(tuple(row) for row in neighbor)
                if neighbor_tuple not in closed_set:
                    heapq.heappush(open_list, (f, neighbor, g + 1, current_state, moved_number, direction))

        return -1  # 無解

    def map_to_direction(self, step_list):
        new_step_list = list()
        for coordinate in step_list:
            if coordinate[1] == (0, -1):
                new_step_list.append([coordinate[0], 'S'])
            if coordinate[1] == (-1, 0):
                new_step_list.append([coordinate[0], 'D'])
            if coordinate[1] == (0, 1):
                new_step_list.append([coordinate[0], 'W'])
            if coordinate[1] == (1, 0):
                new_step_list.append([coordinate[0], 'A'])
        return new_step_list

    # def print_direction(self, step_list):
    #     step_list_revised = []
    #     for i in range(0, len(step_list)):
    #         if step_list[i][1] == (0, -1):
    #             step_list_revised.append((step_list[i][0], "往下"))
    #         if step_list[i][1] == (-1, 0):
    #             step_list_revised.append((step_list[i][0], "往右"))
    #         if step_list[i][1] == (0, 1):
    #             step_list_revised.append((step_list[i][0], "往上"))
    #         if step_list[i][1] == (1, 0):
    #             step_list_revised.append((step_list[i][0], "往左"))
    #     return step_list_revised


    # 執行演算法並列出步驟
    def process(self, initial_state, myCar, goal_position):
        self.initial_state = initial_state
        self.myCar = myCar
        self.m = len(self.initial_state)
        self.n = len(self.initial_state[0])
        self.goal_position = goal_position
        step_list = list()
        move_status = list()
        new_step_list = list()

        # print(f"myCar:{myCar}")
        # print(type(myCar))
        # print(f"goal_position:{goal_position}")
        # print(type(goal_position))
        steps = self.a_star_search(self.initial_state)
        if steps != -1:
            for step, moved_number, direction in steps:
                move_status.append(step)
                if moved_number and direction:
                    step_list.append([moved_number, direction])
            new_step_list = self.map_to_direction(step_list)
        else:
            print("無解")
        return move_status, new_step_list

class EvaluateAlgorithm:
    def __init__(self, obj_temp):
        self.obj_a = obj_temp

    def chooseTheAlgorithm(self, parkinglot):
        occupied_space_list = self.obj_a.secondaryCheck(parkinglot, "inspect")
        if len(occupied_space_list) > 0:
            return "AStar"
        else:
            return "BFS"


class SimplifyRoutes:
    # 幫 step_list 加上一個紀錄指標的欄位，並初始化指標為 0
    def preprocess_the_step_list(self, step_list):
        for each_step in step_list:
            each_step.append(0)
        return step_list

    # 將上下左右轉換成 list可直接加上去的值
    def switch_to_coordinate(self, step_list_direction):
        if step_list_direction == 'S':
            return (1, 0)
        if step_list_direction == 'W':
            return (-1, 0)
        if step_list_direction == 'A':
            return (0, -1)
        if step_list_direction == 'D':
            return (0, 1)

    # 找到特定目標在state裡面的座標
    def find_coordinate(self, state, step_list_element):
        for i in range(0, len(state)):
            for j in range(0, len(state[0])):
                if state[i][j] == step_list_element:
                    return (i, j)

    # 將特定元素在state中從位置A移到位置B (負責實際移動)
    def move_element(self, state, start_position, moving_amount):
        end_position = (start_position[0] + moving_amount[0], start_position[1] + moving_amount[1])
        new_state = deepcopy(state)
        new_state[end_position[0]][end_position[1]], new_state[start_position[0]][start_position[1]] = \
        new_state[start_position[0]][start_position[1]], new_state[end_position[0]][end_position[1]]
        return new_state

    # 幫忙呼叫三個函數來移動車輛 (負責呼叫函數來實際移動)
    def get_new_state(self, order, state, step_list, direction):
        new_state = deepcopy(state)
        if direction == "forward":
            for i in range(0, order + 1):
                start_position = self.find_coordinate(new_state, step_list[i][0])
                moving_amount = self.switch_to_coordinate(step_list[i][1])
                new_state = self.move_element(new_state, start_position, moving_amount)
        if direction == "backward":
            for i in range(0, order):
                start_position = self.find_coordinate(new_state, step_list[i][0])
                moving_amount = self.switch_to_coordinate(step_list[i][1])
                new_state = self.move_element(new_state, start_position, moving_amount)
        # start_position = self.find_coordinate(state, step_list[order][0])
        # moving_amount = self.switch_to_coordinate(step_list[order][1])
        # new_state = self.move_element(state, start_position, moving_amount)
        return new_state

    # 計算起始位置與目標位置
    def calculate_start_end_position(self, order, state, step_list):
        start_position = self.find_coordinate(state, step_list[order][0])
        move_amount = self.switch_to_coordinate(step_list[order][1])
        end_position = (start_position[0] + move_amount[0], start_position[1] + move_amount[1])
        return start_position, end_position

    # 將指定的步驟向前移至指定的位置
    def move_the_step_list(self, from_order, to_order, step_list):
        step = step_list.pop(from_order)
        step_list.insert(to_order, step)
        return step_list

    # 將指定的步驟向後新增至指定的位置，並將原步驟處元素改為"0"
    def insert_the_step_list(self, from_order, to_order, step_list):
        step_list_copied = deepcopy(step_list)
        step_list.insert(to_order, step_list_copied[from_order])
        step_list[from_order][0] = "0"
        return step_list

    # 檢查步驟是否能往前合併 (兩目標步驟中間是否有位置重疊)
    def check_forward_position(self, from_order, to_order, state, step_list):
        # print(f"forward --- from_order's step:{step_list[from_order]}")
        # deepcopy一個模擬狀態，先模擬移動一樣元素的第一步，方可估算後面X步一樣元素的移動位置
        simulation_state = deepcopy(state)
        simulation_state = self.get_new_state(from_order, simulation_state, step_list, "forward")

        target_start_pos, target_end_pos = self.calculate_start_end_position(to_order, simulation_state, step_list)

        same_pos = False  # 初始化
        from_order += 1  # 從目標步驟的下一個開始檢查
        for order in range(from_order, to_order):
            # 計算兩個步驟之間每一個元素的起始位置與目標位置
            start_pos, end_pos = self.calculate_start_end_position(order, simulation_state, step_list)

            # 其中 "有一元素移動前位置" 與 "目標步驟移動後位置" 重疊
            if target_end_pos == start_pos:
                # print(f"forward --- 1：元素移動前 目標移動後：{step_list[order]} vs {step_list[from_order-1]}")
                same_pos = True
                return same_pos
            # 其中 "有一元素移動後位置" 與 "目標步驟移動後位置" 重疊
            elif target_end_pos == end_pos:
                # print(f"forward --- 2：元素移動後 目標移動後：{step_list[order]} vs {step_list[from_order-1]}")
                same_pos = True
                return same_pos
        return same_pos

    # 檢查步驟是否能往後合併 (兩目標步驟中間是否有位置重疊)
    def check_backward_position(self, from_order, to_order, state, step_list):
        # print(f"backward --- from_order's step:{step_list[from_order]}")
        simulation_state = deepcopy(state)
        simulation_state = self.get_new_state(from_order, simulation_state, step_list, "backward")

        target_start_pos, target_end_pos = self.calculate_start_end_position(from_order, simulation_state, step_list)

        same_pos = False  # 初始化
        from_order += 1  # 從目標步驟的下一個開始檢查
        for order in range(from_order, to_order):
            # print(f"backward --- (in for loop) order:{order} step_list[order]:{step_list[order]}")
            # 計算兩個步驟之間每一個元素的起始位置與目標位置
            start_pos, end_pos = self.calculate_start_end_position(order, simulation_state, step_list)
            # 其中 "有一元素移動後位置" 與 "目標步驟移動前位置" 重疊
            if target_start_pos == end_pos:
                # print(f"backward --- 3：元素移動後 目標移動後：{step_list[order]} vs {step_list[from_order-1]}")
                same_pos = True
                return same_pos
            # 其中 "有一元素移動前位置" 與 "目標步驟移動後位置" 重疊
            elif target_end_pos == start_pos:
                # print(f"backward --- 4：元素移動後 目標移動前：{step_list[order]} vs {step_list[from_order-1]}")
                same_pos = True
                return same_pos
        return same_pos

    # 將步驟中含有 "0" 元素的步驟去除並回傳
    def remove_zero_element(self, step_list):
        new_step_list = list()
        for step in step_list:
            if step[0] != '0':
                new_step_list.append(step)
        return new_step_list

    # 列印出移動過程
    def print_the_result(self, result, state, step):
        if result == 'Y':
            print(f"✔ {step}：移動")
            for x in state:
                print(x)
            print("-------------------------------------")
        if result == 'N':
            print(f"✘ {step}：指標滿了！(無移動)")
            for x in state:
                print(x)
            print("-------------------------------------")
        if result == 'E':
            print(f"✔ {step}：提早移動")
            for x in state:
                print(x)
            print("-------------------------------------")
        return

    def execute_the_merger(self, step_list, state):
        i = 0
        # 大迴圈，遍歷每個 step_list 裡面的元素
        while i < len(step_list):
            # 如果指標滿了
            if step_list[i][2] == 1:
                i += 1
                continue

            # 指標還沒滿
            else:
                j = i + 1  # 從特定元素的下一個位置開始檢查
                forward_same_pos = False  # 初始化 (為判斷位置有無重疊的布林直)
                backward_same_pos = False  # 初始化
                already_done = False  # 初始化 ()

                # 如果大迴圈到 step_list 最後一個項目，就不須做後續判斷
                if i == len(step_list) - 1:
                    step_list[i][2] += 1
                    i += 1
                    break

                # 如果下一個元素跟前一個一樣，就直接移動第一步，不用做後續判斷
                elif step_list[j][0] == step_list[i][0]:
                    step_list[i][2] += 1
                    i += 1
                    continue

                else:
                    # 找 i~len(step_list) 之內是否還有跟 each_step[0] 一樣的元素
                    while (j < len(step_list)) and (forward_same_pos == False):

                        # 找到一樣元素且指標沒滿，便計算目標位置
                        if (step_list[j][0] == step_list[i][0]) and (step_list[j][2] == 0):

                            forward_same_pos = self.check_forward_position(i, j, state, step_list)

                            # 若跑完 i+1~j-1 的迴圈後發現不會影響其中元素的移動，則(一樣的元素)提早移動
                            if forward_same_pos == False:
                                step_list[i][2] += 1
                                step_list[j][2] += 1
                                step_list = self.move_the_step_list(j, i + 1, step_list)

                                already_done = True
                                break

                            # 若發現會影響其中元素的移動，則檢查能否延後移動
                            if forward_same_pos == True:
                                backward_same_pos = self.check_backward_position(i, j, state, step_list)

                                # 若跑完 i+1~j-1 的迴圈後發現不會影響其中元素的移動，則(一樣的元素)往後合併
                                if backward_same_pos == False:
                                    step_list = self.insert_the_step_list(i, j, step_list)
                                    already_done = True  # 此處雖然沒有移動，但因為步驟往後插入合併(多一步驟)，所以此目標步驟元素改為"0"，此迴圈不移動
                                    break
                                # 若發現會影響其中元素的移動，跳離 while迴圈，直接進行此步驟移動
                                if backward_same_pos == True:
                                    break

                        # j+1使 while迴圈繼續推進 (用來推進找到一樣的元素)
                        j += 1

                    # 不是最後一個、下一個跟前一個沒有一樣、在 i~len(step_list)之內沒有相同且可以前移或後移的元素
                    if already_done == False:
                        step_list[i][2] += 1
                    i += 1

        step_list = self.remove_zero_element(step_list)
        return state, step_list

    # 整理後步驟輸出，同樣主體存於同一個 list裡面
    def organize_step_output(self, processed_step_list):
        new_list = []
        for num in range(0, len(processed_step_list)):
            if num > 0:
                if processed_step_list[num][0] != processed_step_list[num - 1][0]:
                    new_list.append([processed_step_list[num]])
                else:  # processed_step_list[num][0] == processed_step_list[num-1][0]
                    new_list[-1].append(processed_step_list[num])
            else:  # num==0
                new_list.append([processed_step_list[num]])
        # print("\n整理後步驟輸出(同樣主體存於同一個list裡面)：")
        # for same_car in new_list:
        #     print(same_car)
        return new_list

    def process(self, state, step_list_input):
        # 初始化指標 (全都設為 0)
        step_list = self.preprocess_the_step_list(step_list_input)

        # 核心處理呼叫
        new_state, new_step_list = self.execute_the_merger(step_list, state)
        new_step_list = [[step[0], step[1]] for step in new_step_list]
        return new_step_list
        # print("最終狀態：")
        # for j in new_state:
        #     print(j)
        # print("-------------------------------------")

        # 標準化處理，只印出車輛代號及移動方向，並將移動方向改為 W/S/A/D 輸出
        # processed_step_list = self.standardize_step_list(new_step_list)

        # print("步驟輸出：")
        # print(processed_step_list)

