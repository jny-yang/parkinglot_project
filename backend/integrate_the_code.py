from copy import deepcopy

from park_the_car.py import FindingEmptySpace, CalculateExchangeCount, InspectWholeStatus, AdjustSpaceAllocation
from retrieve_the_car.py import FindingRoute, EvaluateAlgorithm, SimplifyRoutes
from connect_to_database.py import InteractWithDatabase

# 初始化
def initialize():
    global width
    global height
    width = 5
    height = 5
    parkinglot = [[' ' for j in range(0, 5)] for i in range(0, 5)]
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
                print("all_moving_step:")
                print(all_moving_step)


# <取車>
def receiving(parkinglot, entrance, car_id):
    B = CalculateExchangeCount()
    E = FindingRoute()
    G = SimplifyRoutes()
    H = InteractWithDatabase()
    
    moving_status_list = list()
    move_status = list()
    step_list = list()

    parkinglot = H.read(parkinglot)
    print("從資料庫讀出來的停車場:")
    for i in parkinglot:
        print(i)

    # algorithm = F.chooseTheAlgorithm(parkinglot)
    # car_id = input("請輸入要取出的車輛")
    count, moving_step = B.process(parkinglot, car_id, entrance, "counts")
    # if algorithm == "BFS":
    if count == 0:
        print("BFS")
        moving_status_list, step_list = B.process(parkinglot, car_id, entrance, "steps")
        # moving_status_list = moving_status_list[1]
        move_status = moving_status_list[-1]
        H.delete_data(car_id)
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

    print("final state:")
    for i in move_status:
        print(i)
    print(f"step list:{step_list}")
    
    
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
