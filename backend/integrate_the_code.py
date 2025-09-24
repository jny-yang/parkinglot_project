from copy import deepcopy

from park_the_car import FindingEmptySpace, CalculateExchangeCount, InspectWholeStatus, AdjustSpaceAllocation
from retrieve_the_car import FindingRoute, SimplifyRoutes
from connect_to_database import InteractWithDatabase

# 初始化
def initialize():
    global width
    global height
    width = 3
    height = 3
    parkinglot = [[' ' for j in range(0, 3)] for i in range(0, 3)]
    entrance = (len(parkinglot) - 1, len(parkinglot[0]) // 2)
    simulated_parkinglot = deepcopy(parkinglot)
    return parkinglot, simulated_parkinglot, entrance


# <停車>
def parking(parkinglot, entrance, car_id):
    A = FindingEmptySpace()
    B = CalculateExchangeCount()
    C = InspectWholeStatus()
    D = AdjustSpaceAllocation()
    H = InteractWithDatabase()

    keep_searching_space = False
    all_moving_step = list()
    temp_list = list()
    test_list = list()
    final_list = list()
    parkinglot = H.read(parkinglot)
    for i in parkinglot:
        print(i)

    # 取得停車座標
    position = A.process(parkinglot)
    # 初次檢查停車座標是否不須交換直接可到
    if position == -1:
        print("最小停車場單位為3*3")
    elif position == None:
        print("所有停車位皆滿")
    else: # 停車場還有位置
        # car_id = input("請輸入要停放的車輛")
        parkinglot[entrance[0]][entrance[1]] = car_id
        count, moving_step = B.process(parkinglot, car_id, position, "counts")
        if count == 0: # 是，直接執行<停車>
            parkinglot = C.MoveTheCar(parkinglot, entrance, position) # 直接移動
            print(f"停車完後的停車場狀態")
            for i in parkinglot:
                print(i)
            all_moving_step.append(moving_step)
            H.add_single_data(parkinglot, car_id)
            print(f"moving_step:{moving_step}")
            for i in moving_step:
                if i[0] == car_id:
                    temp_list.append(i)
            all_moving_step.append(temp_list)
            print(f"all_moving_step:{all_moving_step}")
            return all_moving_step

        else: # 否，進入後續處理(找尋其他座標)
            keep_searching_space = True
            parkinglot, all_moving_step = D.findAvailableParkingSpace(keep_searching_space, position, parkinglot, car_id)
            if parkinglot == None:
                print("尚未解決滿車移車問題")
            else:
                H.add_single_data(parkinglot, car_id)
                H.transfer_data_to_db(parkinglot)
                for i in parkinglot:
                    print(i)
                for i in all_moving_step:
                    temp_list.append(i[0])
                # print(f"temp_list:{temp_list}")
                for i in temp_list:
                    if i[0] == car_id:
                        test_list.append(i)
                # print(f"test_list:{test_list}")
                final_list.append(temp_list)
                final_list.append(test_list)
                # print(f"final_list:{final_list}")
                return final_list


# <取車>
def retrieving(parkinglot, entrance, car_id):
    B = CalculateExchangeCount()
    E = FindingRoute()
    G = SimplifyRoutes()
    H = InteractWithDatabase()

    moving_status_list = list()
    move_status = list()
    step_list = list()
    temp_list = list()
    final_list = list()
    have_car = False

    parkinglot = H.read(parkinglot)
    print("從資料庫讀出來的停車場:")
    for i in parkinglot:
        print(i)

    for i in range(len(parkinglot)):
        for j in range(len(parkinglot[0])):
            if parkinglot[i][j] == car_id:
                have_car = True
                break
        if have_car == True:
            break

    if have_car == False:
        return -1 # 取不存在停車場中的車

    # algorithm = F.chooseTheAlgorithm(parkinglot)
    # car_id = input("請輸入要取出的車輛")
    count, moving_step = B.process(parkinglot, car_id, entrance, "counts")
    print(f"count:{count}")
    # if algorithm == "BFS":
    if count == 0:
        print("BFS")
        moving_status_list, step_list = B.process(parkinglot, car_id, entrance, "steps")
        # moving_status_list = moving_status_list[1]
        move_status = moving_status_list[-1]
        H.delete_data(car_id)
        for i in step_list:
            if i[0] == car_id:
                temp_list.append(i)
        final_list.append(step_list)
        final_list.append(temp_list)
        print(f"step_list:{step_list}")
        print(f"temp_list:{temp_list}")
        print(f"final_list:{final_list}")
        return final_list
    # if algorithm == "AStar":
    else:
        print("AStar")
        moving_status_list, step_list = E.process(parkinglot, car_id, entrance)
        print(f"step list before move:{step_list}")
        step_list = G.process(parkinglot, step_list)
        move_status = moving_status_list[-1]
        H.transfer_data_to_db(move_status)
        H.delete_data(car_id)
        # for i in moving_status_list:
        #     for j in i:
        #         print(j)
        #     print("-------------------------")
        # print(f"step_list:{step_list}")
        for i in step_list:
            if i[0] == car_id:
                temp_list.append(i)
        final_list.append(step_list)
        final_list.append(temp_list)
        # print(f"temp_list:{temp_list}")
        # print(f"final_list:{final_list}")
        return final_list

    # print("final state:")
    # for i in move_status:
    #     print(i)
    # print(f"step list:{step_list}")


# <檢查>
def inspecting(parkinglot):
    C = InspectWholeStatus()
    H = InteractWithDatabase()

    parkinglot = H.read(parkinglot)
    state_after_move, step_after_move = C.EvaluateMoves(parkinglot)
    H.transfer_data_to_db(state_after_move)
    for i in state_after_move:
        print(i)
    print(f"step:{step_after_move}")



