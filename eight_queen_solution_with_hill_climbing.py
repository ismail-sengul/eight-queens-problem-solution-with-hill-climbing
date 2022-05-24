import random as rd
import timeit

processes = []
def fill_chessboard():
    queens_coordinates = []
    for i in range(8):
        row_select = rd.randint(0, 7)
        queens_coordinates.append(row_select)
    return queens_coordinates

def queen_attack_score(queens_coordinates,x,y):
    attacked = 0
    for i in range(8):
        if i == y:
            continue
        x_queen = queens_coordinates[i]
        if(abs(x_queen - x) == abs(i - y) or x_queen == x):
            attacked += 1
    return attacked
             
def node_attack_score(queens_coordinates):
    h = 0
    for i in range(8):
        x_queen = queens_coordinates[i]
        h += queen_attack_score(queens_coordinates,x_queen,i)
    h /= 2
    return int(h)


def hill_climbing():
    queens_coordinates = fill_chessboard()
    move_count = 0
    random_restart = 0
    h = node_attack_score(queens_coordinates)
    while(True):
        if random_restart != 0:
            queens_coordinates = fill_chessboard()   
            h = node_attack_score(queens_coordinates)
        min_attacked_move = h
        min_attacked_x = queens_coordinates[0]
        min_attacked_y = 0
        while(True):
            for i in range(8):
                x = queens_coordinates[i]
                for j in range(8):
                    queens_coordinates[i] = j
                    if x == j:
                        continue
                    attack_score = node_attack_score(queens_coordinates)
                    if(attack_score == 0):
                        move_count += 1
                        return queens_coordinates, move_count , random_restart
                    if(min_attacked_move > attack_score):
                        min_attacked_move = attack_score
                        min_attacked_y = i
                        min_attacked_x = j
                queens_coordinates[i] = x
            if h == min_attacked_move:
                break
            h = min_attacked_move
            queens_coordinates[min_attacked_y] = min_attacked_x
            move_count += 1
        if h == 0:
            break
        random_restart += 1
    return queens_coordinates,move_count,random_restart

def print_chessboard(queens_coordinates):
    for i in range(8):
        for j in range(8):
            if queens_coordinates[j] == i:
                print("Q", end=" ")
            else:
                print("*",end = " ")
        print()
                
avg_random_restart = 0
avg_move_count = 0
avg_process_time = 0

for i in range(15):
    start_time = timeit.default_timer()
    queens_coordinates, move_count, random_restart = hill_climbing()
    end_time = timeit.default_timer()
    process_time = (end_time - start_time)*1000
    avg_random_restart += random_restart
    avg_move_count += move_count
    avg_process_time += process_time
    process_time = "%.2f" %  process_time + " ms"
    processes.append([move_count,random_restart,process_time])
    print("Solution:",i+1,"\n")
    print_chessboard(queens_coordinates)

avg_move_count = avg_move_count/15
avg_random_restart = avg_random_restart/15
avg_process_time = avg_process_time/15
processes.append([avg_move_count,avg_random_restart,avg_process_time])

print("\n Solution    Move Counts          Random Restart         Process Time",sep = "    ")
print("---------- ----------------   ------------------------   -------------")
for i in range(15):
    print("  {:<10}    {:<25} {:<17} {}".format(i+1, processes[i][0],processes[i][1],processes[i][2]))

print("----------------------------------------------------------------------")
print("Average Move Count: {} \nAverage Random Restart: {} \nAverage Process Time: {} ms"
      .format("%.2f" % processes[15][0],"%.2f" % processes[15][1],"%.2f" % processes[15][2]))
