# 停車
# 依設定順位檢查有無空位。若有，則將入口處車輛移置空位處
# 可以從

from collections import deque
from copy import deepcopy
from retrieve_the_car import FindingRoute

class FindingEmptySpace:

    # constructor初始化
    def __init__(self):
        # self.n = len(parkingLot)  # 停車場寬
        # self.m = len(parkingLot[0])  # 停車場長
        self.empty_space_list = list()
        self.occupied_space_list = list()

    # 檢查第一順位的位置是否有任何空位，若有則回傳空位座標，若無則回傳 None，例外則回傳 -1
    def firstCheck(self, parkingLot, action):
        n = len(parkingLot)
        m = len(parkingLot[0])
        self.empty_space_list = list()

        # 檢查順序：左(由上至下)→右(由上至下)→上(由左至右)→中(由上至下)→中左半(1由上至下/2由左至右)→中右半(1由上至下/2由左至右)→入口左側(由右至左)→入口右側(由左至右)
        if m < 5 and m > 2:
            # 最左側
            for i in range(0, n):
                if parkingLot[i][0] == ' ':
                    print("flag a")
                    if action == "park":
                        return (i, 0)
                    if action == "inspect":
                        self.empty_space_list.append((i,0))
            # 最右側
            for i in range(0, n):
                if parkingLot[i][m - 1] == ' ':
                    print("flag b")
                    if action == "park":
                        return (i, m - 1)
                    if action == "inspect":
                        self.empty_space_list.append((i, m - 1))
            else:
                if action == "park":
                    return None
        elif m < 7:
            # 最左側
            for i in range(0, n):
                if parkingLot[i][0] == ' ':
                    print("flag c")
                    if action == "park":
                        return (i, 0)
                    if action == "inspect":
                        self.empty_space_list.append((i, 0))
            # 最右側
            for i in range(0, n):
                if parkingLot[i][m - 1] == ' ':
                    print("flag d")
                    if action == "park":
                        return (i, m - 1)
                    if action == "inspect":
                        self.empty_space_list.append((i, m - 1))
            # 中間(包含最上側)
            for i in range(2, m - 2):
                for j in range(0, n - 1):
                    if parkingLot[j][i] == ' ':
                        print("flag e")
                        if action == "park":
                            return (j, i)
                        if action == "inspect":
                            self.empty_space_list.append((j, i))
            else:
                if action == "park":
                    return None
        elif m == 7:
            print("m=7")
            # 最左側
            for i in range(0, n):
                if parkingLot[i][0] == ' ':
                    print("flag f")
                    if action == "park":
                        return (i, 0)
                    if action == "inspect":
                        self.empty_space_list.append((i, 0))
            # 最右側
            for i in range(0, n):
                if parkingLot[i][m - 1] == ' ':
                    print("flag g")
                    if action == "park":
                        return (i, m - 1)
                    if action == "inspect":
                        self.empty_space_list.append((i, m - 1))
            # 最上側
            for i in range(2, m - 2):
                if parkingLot[0][i] == ' ':
                    print("flag h")
                    if action == "park":
                        return (0, i)
                    if action == "inspect":
                        self.empty_space_list.append((0, i))
            # 中間
            for i in [2, m - 3]:
                for j in range(1, n - 1):
                    if parkingLot[j][i] == ' ':
                        print("flag i")
                        if action == "park":
                            return (j, i)
                        if action == "inspect":
                            self.empty_space_list.append((j, i))
            else:
                if action == "park":
                    return None
        elif m > 7:
            # 最左側
            for i in range(0, n):
                if parkingLot[i][0] == ' ':
                    print("flag j")
                    if action == "park":
                        return (i, 0)
                    if action == "inspect":
                        self.empty_space_list.append((i, 0))
            # 最右側
            for i in range(0, n):
                if parkingLot[i][m - 1] == ' ':
                    print("flag k")
                    if action == "park":
                        return (i, m - 1)
                    if action == "inspect":
                        self.empty_space_list.append((i, m - 1))
            # 最上側
            for i in range(2, m - 2):
                if parkingLot[0][i] == ' ':
                    print("flag l")
                    if action == "park":
                        return (0, i)
                    if action == "inspect":
                        self.empty_space_list.append((0, i))
            # 中間
            x = n // 3  # 用來表示分割成幾個 三個一組步驟(step1,2,3) 的單位
            y = 0  # 初始化計次變數

            # 中左半
            for i in range(0, n - 1, 3):  # n-1:行數不包含入口那行
                # 判斷步驟單位是否超出次數
                if y < x:
                    # step1(b頭頂)
                    if y < x - 1 or (n % 3 == 0 or n % 3 == 1 or n % 3 == 2):
                        if parkingLot[i + 1][2] == ' ':
                            print("flag m")
                            if action == "park":
                                return (i + 1, 2)
                            if action == "inspect":
                                self.empty_space_list.append((i + 1, 2))

                    # step2(b上橫)
                    if y < x - 1 or (n % 3 == 1 or n % 3 == 2):
                        for j in range(2, m // 2):
                            if parkingLot[i + 2][j] == ' ':
                                print("flag n")
                                if action == "park":
                                    return (i + 2, j)
                                if action == "inspect":
                                    self.empty_space_list.append((i + 2, j))
                    # step3(b下橫)
                    if y < x - 1 or (n % 3 == 2):
                        for j in range(2, m // 2):
                            if parkingLot[i + 3][j] == ' ':
                                print("flag o")
                                if action == "park":
                                    return (i + 3, j)
                                if action == "inspect":
                                    self.empty_space_list.append((i + 3, j))
                    y += 1

            y = 0  # 重新初始化

            # 中右半
            for i in range(0, n - 1, 3):
                # 判斷步驟單位是否超出次數
                if y < x:
                    # step1(b頭頂)
                    if y < x - 1 or (n % 3 == 0 or n % 3 == 1 or n % 3 == 2):
                        if parkingLot[i + 1][m - 3] == ' ':
                            print("flag p")
                            if action == "park":
                                return (i + 1, m - 3)
                            if action == "inspect":
                                self.empty_space_list.append((i + 1, m - 3))

                    # step2(b上橫)
                    if y < x - 1 or (n % 3 == 1 or n % 3 == 2):
                        for j in range(m - 3, m // 2, -1):
                            if parkingLot[i + 2][j] == ' ':
                                print("flag q")
                                if action == "park":
                                    return (i + 2, j)
                                if action == "inspect":
                                    self.empty_space_list.append((i + 2, j))
                    # step3(b下橫)
                    if y < x - 1 or (n % 3 == 2):
                        for j in range(m - 3, m // 2, -1):
                            if parkingLot[i + 3][j] == ' ':
                                print("flag r")
                                if action == "park":
                                    return (i + 3, j)
                                if action == "inspect":
                                    self.empty_space_list.append((i + 3, j))
                    y += 1

            # 入口左右兩側
            if n % 3 == 0:
                # 從入口往左數，逐漸遞減
                if m % 2 != 0:  # m為奇數
                    for i in range(m // 2 - 1, m // 2 - ((m - 9) // 2) - 1, -1):
                        if parkingLot[n - 1][i] == ' ':
                            print("flag s")
                            if action == "park":
                                return (n - 1, i)
                            if action == "inspect":
                                self.empty_space_list.append((n - 1, i))
                else:  # m為偶數
                    for i in range(m // 2 - 1, m // 2 - ((m - 8) // 2) - 1, -1):
                        if parkingLot[n - 1][i] == ' ':
                            print("flag t")
                            if action == "park":
                                return (n - 1, i)
                            if action == "inspect":
                                self.empty_space_list.append((n - 1, i))

                # 從入口往右數，逐漸遞增
                for i in range(m // 2 + 1, m // 2 + ((m - 9) // 2) + 1):
                    if parkingLot[n - 1][i] == ' ':
                        print("flag u")
                        if action == "park":
                            return (n - 1, i)
                        if action == "inspect":
                            self.empty_space_list.append((n - 1, i))
            else: # 沒有找到空位
                if action == "park":
                    return None

        else:  # m < 3 exception
            if action == "park":
                return -1

        if action == "inspect":
            return self.empty_space_list

    # 檢查第二順位的位置是否有任何空位，若有則回傳空位座標，若無則回傳 None，例外則回傳 -1
    def secondaryCheck(self, parkingLot, action):
        # 取得停車場長寬
        n = len(parkingLot)
        m = len(parkingLot[0])
        self.occupied_space_list = list()

        if m == 3:
            # 中間 (由上而下)
            for i in range(0, m - 1):
                if (action == "park") and (parkingLot[i][1] == ' '):
                    print("flag ba")
                    return (i, 1)
                if (action == "inspect") and (parkingLot[i][1] != ' '):
                    print("flag baa")
                    self.occupied_space_list.append([parkingLot[i][1], (i, 1)])
            else:
                if action == "park":
                    print("flag ca")
                    return None
        elif m == 4:
            # 最下側 (只有一格)
            if (action == "park") and (parkingLot[n - 1][m // 2 - 1] == ' '):
                print("flag da")
                return (n - 1, m // 2 - 1)
            if (action == "inspect") and (parkingLot[n - 1][m // 2 - 1] != ' '):
                print("flag daa")
                self.occupied_space_list.append([parkingLot[n - 1][m // 2 - 1], (n - 1, m // 2 - 1)])
            # 中間 (由上而下、由左而右)
            for i in range(0, m - 1):
                for j in range(1, m - 1):
                    if (action == "park") and (parkingLot[i][j] == ' '):
                        print("flag ea")
                        return (i, j)
                    if (action == "inspect") and (parkingLot[i][j] != ' '):
                        print("flag eaa")
                        self.occupied_space_list.append([parkingLot[i][j], (i, j)])
            else:
                if action == "park":
                    print("flag fa")
                    return None
        elif m < 7:
            # 左側與右側 (由左而右、由上而下)
            for i in range(0, n - 1):
                for j in [1, m - 2]:
                    if (action == "park") and (parkingLot[i][j] == ' '):
                        print("flag ga")
                        return (i, j)
                    if (action == "inspect") and (parkingLot[i][j] != ' '):
                        print("flag gaa")
                        self.occupied_space_list.append([parkingLot[i][j], (i, j)])
            # 最下側最靠左、右格
            for i in [1, m - 2]:
                if (action == "park") and (parkingLot[n - 1][i] == ' '):
                    print("flag ha")
                    return (n - 1, i)
                if (action == "inspect") and (parkingLot[n - 1][i] != ' '):
                    print("flag haa")
                    self.occupied_space_list.append([parkingLot[n - 1][i], (n - 1, i)])
            # 最下側入口以左一格
            if m == 6:
                if (action == "park") and (parkingLot[n - 1][2] == ' '):
                    print("flag ia")
                    return (n - 1, 2)
                if (action == "inspect") and (parkingLot[n - 1][2] != ' '):
                    print("flag iaa")
                    self.occupied_space_list.append([parkingLot[n - 1][2], (n - 1, 2)])
                else:
                    print("flag ja")
                    return None
            else:
                if action == "park":
                    print("flag ka")
                    return None
        elif m == 7:
            # 中間 (由上而下)
            for i in range(1, n - 1):
                if (action == "park") and (parkingLot[i][m // 2] == ' '):
                    print("flag la")
                    return (i, m // 2)
                if (action == "inspect") and (parkingLot[i][m // 2] != ' '):
                    print("flag laa")
                    self.occupied_space_list.append([parkingLot[i][m // 2], (i, m // 2)])
            # 左側與右側 (由上而下)
            for i in range(0, n - 1):
                for j in [1, m - 2]:
                    if (action == "park") and (parkingLot[i][j] == ' '):
                        print("flag ma")
                        return (i, j)
                    if (action == "inspect") and (parkingLot[i][j] != ' '):
                        print("flag maa")
                        self.occupied_space_list.append([parkingLot[i][j], (i, j)])
            # 最下側 (左右左右順序)
            for i in [1, 5, 2, 4]:
                print(f"i={i}")
                if (action == "park") and (parkingLot[n - 1][i] == ' '):
                    print("flag na")
                    return (n - 1, i)
                if (action == "inspect") and (parkingLot[n - 1][i] != ' '):
                    print("flag naa")
                    self.occupied_space_list.append([parkingLot[n - 1][i], (n - 1, i)])
                    # print(f"occupied_space_list:{self.occupied_space_list}")
            else:
                if action == "park":
                    print("flag oa")
                    return None
        elif m > 7:
            # p:用來計算迴圈次數(入口上一排可放or不可放)
            if m > 9 and n % 3 == 0:
                p = n - 2
            else:
                p = n - 1

            # 中間
            x = n // 3  # 用來表示分割成幾個 三個一組步驟(step1,2,3) 的單位
            y = 0  # 初始化計次變數
            for i in range(1, p, 3):  # 奇偶數p值不同
                # 判斷步驟單位是否超出次數
                if y < x:
                    # 最後一圈之前的所有：用y<x-1判斷；最後一圈：用n%3判斷
                    # step1(T上橫): 左右左右順序
                    if y < x - 1 or (n % 3 == 0 or n % 3 == 1 or n % 3 == 2):
                        for j in range(3, m // 2 + 1):
                            if (action == "park") and (parkingLot[i][j] == ' '):
                                print("flag pa")
                                return (i, j)
                            if (action == "inspect") and (parkingLot[i][j] != ' '):
                                print("flag paa")
                                self.occupied_space_list.append([parkingLot[i][j], (i, j)])

                            if (action == "park") and (parkingLot[i][m - 1 - j] == ' '):
                                print("flag qa")
                                return (i, m - 1 - j)
                            if (action == "inspect") and (parkingLot[i][m - 1 - j] != ' '):
                                print("flag qaa")
                                self.occupied_space_list.append([parkingLot[i][m - 1 - j], (i, m - 1 - j)])

                    # step2(T中段): 僅一格
                    if y < x - 1 or (n % 3 == 1 or n % 3 == 2):
                        if (action == "park") and (parkingLot[i + 1][m // 2] == ' '):
                            print("flag ra")
                            return (i + 1, m // 2)
                        if (action == "inspect") and (parkingLot[i + 1][m // 2] != ' '):
                            print("flag raa")
                            self.occupied_space_list.append([parkingLot[i + 1][m // 2], (i + 1, m // 2)])
                    # step3(T下段): 僅一格
                    if y < x - 1 or (n % 3 == 2):
                        if (action == "park") and (parkingLot[i + 2][m // 2] == ' '):
                            print("flag sa")
                            return (i + 2, m // 2)
                        if (action == "inspect") and (parkingLot[i + 2][m // 2] != ' '):
                            print("flag saa")
                            self.occupied_space_list.append([parkingLot[i + 2][m // 2], (i + 2, m // 2)])
                    y += 1

            # 左側與右側 (由上而下)
            for i in range(0, n - 1):
                for j in [1, m - 2]:
                    if (action == "park") and (parkingLot[i][j] == ' '):
                        print("flag ta")
                        return (i, j)
                    if (action == "inspect") and (parkingLot[i][j] != ' '):
                        print("flag taa")
                        self.occupied_space_list.append([parkingLot[i][j], (i, j)])

            # 最下側、(部分條件)入口上側一排 (左右左右順序)
            if n % 3 == 0:  # step1(入口兩側已有放車&&入口上側一排未檢查)
                for i in range(1, 4):  # 入口左右側(各三格)
                    if (action == "park") and (parkingLot[n - 1][i] == ' '): # 入口左側
                        print("flag ua")
                        return (n - 1, i)
                    if (action == "inspect") and (parkingLot[n - 1][i] != ' '): # 入口左側
                        print("flag uaa")
                        self.occupied_space_list.append([parkingLot[n - 1][i], (n - 1, i)])

                    if (action == "park") and (parkingLot[n - 1][m - 1 - i] == ' '): # 入口右側
                        print("flag va")
                        return (n - 1, m - 1 - i)
                    if (action == "inspect") and (parkingLot[n - 1][m - 1 - i] != ' '): # 入口右側
                        print("flag vaa")
                        self.occupied_space_list.append([parkingLot[n - 1][m - 1 - i], (n - 1, m - 1 - i)])
                for i in range(3, m // 2 + 1):  # 入口上側一排
                    if (action == "park") and (parkingLot[n - 2][i] == ' '): # 入口右側
                        print("flag wa")
                        return (n - 2, i)
                    if (action == "inspect") and (parkingLot[n - 2][i] != ' '): # 入口右側
                        print("flag waa")
                        self.occupied_space_list.append([parkingLot[n - 2][i], (n - 2, i)])

                    if (action == "park") and (parkingLot[n - 2][m - 1 - i] == ' '):
                        print("flag xa")
                        return (n - 2, m - 1 - i)
                    if (action == "inspect") and (parkingLot[n - 2][m - 1 - i] != ' '):
                        print("flag xaa")
                        self.occupied_space_list.append([parkingLot[n - 2][m - 1 - i], (n - 2, m - 1 - i)])
            elif n % 3 != 0:  # step2,3(入口兩側未放車)
                for i in range(1, m // 2): # 入口左側
                    if (action == "park") and (parkingLot[n - 1][i] == ' '):
                        print("flag ya")
                        return (n - 1, i)
                    if (action == "inspect") and (parkingLot[n - 1][i] != ' '):
                        print("flag yaa")
                        self.occupied_space_list.append([parkingLot[n - 1][i], (n - 1, i)])
                for i in range(m - 2, m // 2, -1): # 入口右側
                    if (action == "park") and (parkingLot[n - 1][i] == ' '):
                        print("flag za")
                        return (n - 1, i)
                    if (action == "inspect") and (parkingLot[n - 1][i] != ' '):
                        print("flag zaa")
                        self.occupied_space_list.append([parkingLot[n - 1][i], (n - 1, i)])
            else:
                print("flag ab")
                if action == "park":
                    return None

        else:  # m < 3 exception
            if action == "park":
                return -1

        if action == "inspect":
            # print(f"final_occupied_space_list:{self.occupied_space_list}")
            return self.occupied_space_list

    # 主程式進入點
    def process(self, parkingLot):
        result = self.firstCheck(parkingLot, "park")
        if result is None:  # 第一順位已滿
            result = self.secondaryCheck(parkingLot, "park")
        return result


class CalculateExchangeCount:
    # 找車子位置
    def find_car(self, state, car_id):
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] == car_id:
                    return (i, j)
        return None

    # 將 state 轉 tuple（方便存到 set 判斷 visited）
    def state_to_tuple(self, state):
        return tuple(tuple(row) for row in state)

    # 印出狀態
    def print_state(self, state):
        for row in state:
            print(row)
        print()

    def print_move_car_direction(self, before_state, after_state, moved_car):
        before = self.find_car(before_state, moved_car)
        after = self.find_car(after_state, moved_car)
        compare = (after[0] - before[0], after[1] - before[1])
        if compare[1] == -1:
            return 'A'
        if compare[1] == 1:
            return 'D'
        if compare[0] == 1:
            return 'S'
        if compare[0] == -1:
            return 'W'

    def get_moving_step(self, path, moved_car):
        step_list = list()
        for i in range(0, len(path) - 1):
            direction = self.print_move_car_direction(path[i], path[i + 1], moved_car)
            step_list.append([moved_car, direction])
        return step_list

    # BFS
    def bfs_search(self, start_state, target_car_id, destination):
        start_pos = self.find_car(start_state, target_car_id)
        if start_pos == None:
            return None, None  # 找不到
        q = deque()
        visited = set()

        # queue: (state, car_pos, swap_count, path)
        q.append((start_state, start_pos, 0, []))
        visited.add(self.state_to_tuple(start_state))

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # 下、上、右、左

        while q:
            state, (x, y), swap_count, path = q.popleft()
            goal_x, goal_y = destination
            # 檢查是否到達指定位置
            if (x, y) == (goal_x, goal_y):
                return swap_count, path + [state]

            # 嘗試四個方向移動
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(state) and 0 <= ny < len(state[0]):
                    if state[nx][ny] == ' ':  # 只能和空白交換
                        new_state = deepcopy(state)
                        # 交換目標車與空白
                        new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]

                        state_key = self.state_to_tuple(new_state)
                        if state_key not in visited:
                            visited.add(state_key)
                            q.append((new_state, (nx, ny), swap_count, path + [state]))

        return None, None  # 找不到

    def process(self, start_state, target_car_id, destination, result):
        print("start_state:")
        for i in start_state:
            print(i)
        solution = self.bfs_search(start_state, target_car_id, destination)
        swaps, path = solution
        if swaps != None and path != None:
            moving_step = self.get_moving_step(path, target_car_id)
            if result == "counts":
                return solution[0], moving_step
            if result == "steps":
                return solution[1], moving_step
        else:
            return None, None



class InspectWholeStatus:
    def __init__(self):
        self.obj_a = None
        self.obj_b = CalculateExchangeCount()
        self.parkingLot = None

    # 回傳"第一順位中的空位"
    def GetFirstCheckedList(self):
        empty_space_list = self.obj_a.firstCheck(self.parkingLot, "inspect")
        return empty_space_list

    # 回傳"第二順位中已被停車的位置(非空位)"
    def GetSecondaryCheckedList(self):
        occupied_space_list = self.obj_a.secondaryCheck(self.parkingLot, "inspect")
        return occupied_space_list

    # 將停車場中某一位置車輛直接放入另一位置，並回傳新停車場狀態
    def MoveTheCar(self, parkingLot, start, end):
        x1, y1 = start
        x2, y2 = end
        parkingLot[x2][y2] = parkingLot[x1][y1]
        parkingLot[x1][y1] = ' '
        return parkingLot

    # 檢查是否有第二順位車輛可移至第一順位空位，若有則移動，最後回傳"移動後停車場狀態"+"移動步驟"
    def EvaluateMoves(self, parkingLot):
        self.parkingLot = parkingLot
        self.obj_a = FindingEmptySpace()
        empty_space_list = self.GetFirstCheckedList()
        occupied_space_list = self.GetSecondaryCheckedList()
        all_moving_step = list()

        if (empty_space_list != None) and (empty_space_list != -1):
            if (occupied_space_list != None) and (occupied_space_list != -1):
                empty_space_list_copy = deepcopy(empty_space_list)
                for i in empty_space_list_copy:
                    for num, j in enumerate(occupied_space_list):
                        if j != -1:  # 第二順位中尚存的車輛(-1代表已放入第一順位)
                            exchange_count, moving_step = self.obj_b.process(self.parkingLot, j[0], i, "counts")

                            # 不需要任何交換次數者，可將(第二順位中)車輛移動至(第一順位的)空位
                            if exchange_count == 0:
                                # print("-----------------------------------------")
                                # print(f"{j[0]} 可以從 {j[1]} 移到 {i}")
                                self.parkingLot = self.MoveTheCar(self.parkingLot, j[1], i)
                                all_moving_step.append(moving_step)
                                occupied_space_list[num] = -1 # 第二順位中已放入第一順位者list中改為-1
                                empty_space_list.remove(i)
                                break

        # occupied_space_list = [k for k in occupied_space_list if k != -1]
        # print(f"剩下的第一順位空格{empty_space_list}")
        # print(f"剩下的第二順位車位{occupied_space_list}")
        return self.parkingLot, all_moving_step


class AdjustSpaceAllocation:
    def __init__(self):
        self.obj_a = FindingEmptySpace()
        self.obj_b = CalculateExchangeCount()
        self.obj_c = InspectWholeStatus()


    def getSpaceAndCarList(self):
        empty_space = self.obj_a.firstCheck(self.parkingLot, "park")
        if empty_space == None:
            empty_space = self.obj_a.secondaryCheck(self.parkingLot, "park")
        car_list = self.obj_a.secondaryCheck(self.parkingLot, "inspect")
        return empty_space, car_list

    def organizeParkingSpace(self, parkingLot, moved_car_list, all_moving_step):
        self.parkingLot = parkingLot
        empty_space, car_list = self.getSpaceAndCarList()
        # 初始化一個計次指標 car[2] = 0
        for car in car_list:
            car.append(0)
        # 若車輛有移動過，指標改 1
        for car in car_list:
            if car[0] in moved_car_list:
                car[2] = 1
        for position in car_list:
            # 沒有移動過的車
            if position[2] == 0:
                count, moving_step = self.obj_b.process(self.parkingLot, position[0], empty_space, "counts")
                if count == 0:
                    new_parkingLot = self.obj_c.MoveTheCar(self.parkingLot, position[1], empty_space)
                    all_moving_step.append(moving_step)
                    return new_parkingLot, position[0], all_moving_step
                else:
                    continue
            else:
                return None, None, None

    # 有位置但不能直接停車(需要交換次數)的後續處理
    def findAvailableParkingSpace(self, keep_searching_space, position, parkinglot, car_id):
        entrance = (len(parkinglot) - 1, len(parkinglot[0]) // 2)
        moved_car_list = list()
        all_moving_step = list()
        simulated_parkinglot = deepcopy(parkinglot)

        while keep_searching_space:
            pos_x, pos_y = position
            simulated_parkinglot[pos_x][pos_y] = '_'  # _ 在複製的模擬停車場中代表模擬成有車的位置
            position = self.obj_a.process(simulated_parkinglot)  # 將不可直接到位置模擬成有車位置，二次(or more)找尋停車座標
            # 停車場內還有停車位但無直接可到(不須教壞次數)的車位
            if position == None:  # 沒找到位置，所以需要整理
                parkinglot, moved_car, all_moving_step = self.organizeParkingSpace(parkinglot, moved_car_list, all_moving_step)
                if parkinglot == None:
                    print("尚未解決滿車移車問題")
                    return None, None
                moved_car_list.append(moved_car)  # 有移動過的車必須加入moved_car_list
                simulated_parkinglot = deepcopy(parkinglot)
                position = self.obj_a.process(simulated_parkinglot)
                count, moving_step = self.obj_b.process(simulated_parkinglot, car_id, position, "counts")
                if count == 0:
                    parkinglot = self.obj_c.MoveTheCar(parkinglot, entrance, position)  # 直接移動
                    all_moving_step.append(moving_step)
                    keep_searching_space = False
                else:
                    continue
            # 得到二次(or more)座標後
            else:
                count, moving_step = self.obj_b.process(simulated_parkinglot, car_id, position, "counts")  # 計算二次(or more)座標的交換次數
                # 找到其餘不須交換次數的車位
                if count == 0:
                    parkinglot = self.obj_c.MoveTheCar(parkinglot, entrance, position)  # 直接移動
                    all_moving_step.append(moving_step)
                    keep_searching_space = False
                # 找到的車位還是需要交換次數
                else:
                    continue

        return parkinglot, all_moving_step







