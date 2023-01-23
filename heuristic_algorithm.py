import random
import math
from copy import deepcopy
board_width = 9
board_height = 12
#The alphabet with letters proportioned
letters_proportioned = "aaaaaaaabcccddddeeeeeeeeeeeffgghhhhhhiiiiiijkllllmmnnnnnnoooooooppqrrrrrrsssssstttttttttuuuvwwxyyz"
points = [("a",1),("b",3),("c",3),("d",2),("e",1),("f",4),("g",2),("h",4),("i",3),("j",8),("k",5),("l",5),("m",3),("n",2),("o",1),("p",3),("q",10),("r",1),("s",1),("t",1),("u",2),("v",4),("w",4),("x",8),("y",4),("z",10)]
new_points = [("a",1.06951871657754),("b",11.5830115830116),("c",10.03344482),("d",5.277044855),("e",0.998003992),("f",21.3903743315508),("g",7.518796992),("h",14.3884892086331),("i",5.172413793),("j",153.8461538),("k",20.16129032),("l",9.842519685),("m",9.554140127),("n",4.454342984),("o",1.394700139),("p",9.287925697),("q",625),("r",1.650165017),("s",1.03950104),("t",1.98412698412698),("u",4.987531172),("v",37.03703704),("w",22.34636872),("x",173.913043478261),("y",12.9032258064516),("z",138.8888889)]
letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
works = []
number_left_array = []
letters_left_percentage = []
points_percentage = []
points_p = [0]
letters_p = [board_height*board_width]
board  = []
best_score_tree = []
best_word = ""
current_word = "zzzzzz"
best_score = 0
found_word = 0
final_score = 0
board_finished = 0
change_method = 0

def open_file(filename = "altered_points_3_6.txt"):
    file = open(filename, "r")
    contents = file.read()
    global dictionary
    dictionary = contents.splitlines()
    file.close()

def open_file_new(filename = "altered_points_2.txt"):
    file = open(filename, "r")
    contents = file.read()
    global dictionary
    dictionary = contents.splitlines()
    file.close()
def sort_dictionary_new(dictionary):
    i = 0
    for word in dictionary:
        word = word.lower()
        dictionary[i] = dictionary[i].lower()
        point = 0
        dictionary[i] = [dictionary[i]]
        for letter in word:
            for item in new_points:
                if item[0] == letter:
                    point += item[1]
        point *= len(word)
        dictionary[i].append(point)
        i+=1
    dictionary.sort(key=lambda s: s[1], reverse=True)
def sort_dictionary(dictionary):
    i = 0
    for word in dictionary:
        word = word.lower()
        dictionary[i] = dictionary[i].lower()
        point = 0
        dictionary[i] = [dictionary[i]]
        for letter in word:
            for item in points:
                if item[0] == letter:
                    point += item[1]
        point *= len(word)
        dictionary[i].append(point)
        i+=1
    dictionary.sort(key=lambda s: s[1], reverse=True)

def remove_short_words_new(dictionary):
    for i in range(len(dictionary)):
        dictionary[i] = dictionary[i][0]
    remove_list = []
    for word in dictionary:
        if len(word) <= 2:
            remove_list.append(word)
    for word in remove_list:
        dictionary.remove(word)
        
def remove_short_words(dictionary):
    for i in range(len(dictionary)):
        dictionary[i] = dictionary[i][0]
    remove_list = []
    for word in dictionary:
        if len(word) <= 2 or len(word) >= 5:
            remove_list.append(word)
    for word in remove_list:
        dictionary.remove(word)
        
def create_board():
    global board
    global letters_left
    board = []
    for i in range(board_height):
        board.append([])
    #Creates the board
    #start_time = time.perf_counter()
    for i in range(board_height):
        for j in range(board_width):
            board[i].append(random.choice(letters_proportioned))
    letters_left = board_height*board_width

def double_letters_missing(letters = letters, board = board):
    global double_letters_not_on_board
    double_letters_not_on_board = []
    for i in range(26):
        for j in range(26):
            double_letters_not_on_board.append(letters[i]+letters[j])
    for i in range(len(board)):
        for j in range(len(board[i])):
            for k in range(8):
                down = 0
                right = 0
                if k < 3:
                    down = -1
                if k > 4:
                    down = 1
                if k in (0, 3, 5):
                    right = -1
                if k in (2, 4, 7):
                    right = 1
                if 0<=i+down<=len(board)-1 and 0<=j+right<=len(board[i])-1:
                    if board[i][j]+board[i+down][j+right] in double_letters_not_on_board:
                        double_letters_not_on_board.remove(board[i][j]+board[i+down][j+right])


def check_word(current_word = current_word, board = board, found_word = 0, best_score = best_score, best_word = best_word, best_score_tree = best_score_tree, works = works):
    global point
    global acc_point
    point = 0
    acc_point = 0
    global list_of_paths
    list_of_paths = []
    on_board = 1
    for i in range(len(current_word)-1):
        if current_word[i]+current_word[i+1] in double_letters_not_on_board:
            on_board = 0
    if on_board == 1:
        locations = []
        for i in range(len(current_word)):
            locations.append([current_word[i],[]])
            for j in range(len(board)):
                for k in range(len(board[j])):
                    if board[j][k] == current_word[i]:
                        locations[i][1].append([j,k])
        tree = []
        for i in range(len(current_word)-1):
            tree.append([i,[]])
            for j in range(len(locations[i][1])):
                for k in range(len(locations[i+1][1])):
                    if abs(locations[i][1][j][0]-locations[i+1][1][k][0])<=1 and  abs(locations[i][1][j][1]-locations[i+1][1][k][1])<=1 and not ((locations[i][1][j][0]-locations[i+1][1][k][0]) == 0 and  abs(locations[i][1][j][1]-locations[i+1][1][k][1]) == 0):
                        tree[i][1].append([j,k])
        for i in tree[0][1]:
            list_of_paths.append(i)
        for i in range(1, len(tree)):
            for k in range(len(list_of_paths)):
                for j in range(len(tree[i][1])):
                    try:
                        if list_of_paths[k][i] == tree[i][1][j][0]:
                            if len(list_of_paths[k]) == i+1:
                                list_of_paths[k].append(tree[i][1][j][1])
                            elif len(list_of_paths[k]) == i+2:
                                new_path = list(list_of_paths[k])
                                new_path[-1] = tree[i][1][j][1]
                                list_of_paths.append(new_path)
                    except IndexError:
                        continue
        remove_list = []
        for i in range(len(list_of_paths)):
            if len(list_of_paths[i]) != len(current_word):
                remove_list.append(list_of_paths[i])
        for i in range(len(remove_list)):
            if remove_list[i] in list_of_paths:
                list_of_paths.remove(remove_list[i])
        for k in range(len(current_word)-2):
            for i in range(len(current_word)-(k+2)):
                if current_word[i] == current_word[i+k+2]:
                    for j in range(len(list_of_paths)):
                        if list_of_paths[j][i] == list_of_paths[j][i+k+2]:
                            remove_list.append(list_of_paths[j])
        for i in range(len(remove_list)):
            if remove_list[i] in list_of_paths:
                list_of_paths.remove(remove_list[i])
    if list_of_paths != []:
        for letter in current_word:
            if change_method == 0:
                temp_iter = 0
                for item in new_points:
                    temp_iter += 1
                    if item[0] == letter:
                        point += item[1]
                        acc_point += points[temp_iter-1][1]
            elif change_method == 1:
                for item in points:
                    if item[0] == letter:
                        point += item[1]
        point *= len(current_word)
        acc_point *= len(current_word)
        works.append([current_word, point, list_of_paths])

def remove_word(best_word = best_word, best_score_tree = best_score_tree, board = board):
    for i in range(len(best_word)):
        letter = best_word[i]
        order = best_score_tree[0][i] + 1
        occurence_number = 0
        for j in range(len(board)):
            for k in range(len(board[j])):
                if letter in board[j][k]:
                    occurence_number += 1
                if occurence_number == order:
                    board[j][k] += '-'
                    occurence_number += 1
    for i in range(len(board)):
        for j in range(len(board[i])):
            if '-' in board[i][j]:
                board[i][j] = ' '
    column_number = 0
    while column_number < len(board[0]):
        for i in range(len(board)):
            if board[len(board) - i - 1][column_number] == ' ':
                number_up = 0
                above_letter = ' '
                while above_letter == ' ' and number_up <= len(board) -2 - i:
                    above_letter = board[len(board) - i - number_up - 2][column_number]
                    number_up += 1
                board[len(board) - i - 1][column_number] = above_letter
                if above_letter != " ":
                    board[len(board) - i - 1 - number_up][column_number] = ' '
        column_number += 1
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][len(board[i]) - j - 1] == ' ':
                number_up = 0
                above_letter = ' '
                while above_letter == ' ' and number_up <= len(board[i]) -2 - j:
                    above_letter = board[i][len(board[i]) - j - number_up - 2]
                    number_up += 1
                board[i][len(board[i]) - j - 1] = above_letter
                if above_letter != " ":
                    board[i][len(board[i]) - j - 1 - number_up] = ' '
def find_vowel_ratio(board = board):
    global vowel_ratio
    vowel_ratio = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == "a" or board[i][j] == "e" or board[i][j] == "i" or board[i][j] == "o" or board[i][j] == "u" or board[i][j] == "y":
                vowel_ratio += 1
    vowel_ratio = vowel_ratio/(0.01+(letters_left-len(current_word)))
    return vowel_ratio

def check_connectivity(board = board):
    global connectivity
    connectivity = 0.0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] in letters:
                temp_connect = 0
                for k in range(8):    
                    down = 0
                    right = 0
                    if k < 3:
                        down = -1
                    if k > 4:
                        down = 1
                    if k in (0, 3, 5):
                        right = -1
                    if k in (2, 4, 7):
                        right = 1
                    if 0<=i+down<=len(board)-1 and 0<=j+right<=len(board[i])-1:
                        if board[i][j] in letters:
                            temp_connect += 1
                connectivity += temp_connect**2
    connectivity = connectivity/(0.01+(letters_left-len(current_word)))
    return connectivity

open_file_new()
sort_dictionary_new(dictionary)
remove_short_words_new(dictionary)
for everything in range(25):
    create_board()
    find_vowel_ratio()
    while board_finished == 0:
        for i in board:
            print(i)
    #    if letters_left <= 105 and change_method == 0:
    #        change_method = 1
    #        open_file()
    #        sort_dictionary(dictionary)
    #        remove_short_words(dictionary)
    #        three_move(board = board, works = works, letters_left = letters_left, dictionary = dictionary, letters = letters, current_word = current_word, found_word = 0, best_score = best_score, best_word = best_word, best_score_tree = best_score_tree)
        double_letters_missing(board = board)
        best_score = 0
        acc_best_score = 0
        best_word = ""
        best_score_tree = []
        found_word = 0
        iterate = -1
        potentials = []
#        while found_word <= 20:
        while iterate < len(dictionary):
            iterate += 1
            try:
                current_word = dictionary[iterate]
            except IndexError:
                found_word = 21
                break
            check_word(current_word = dictionary[iterate], board = board, found_word = found_word, best_score = best_score, best_word = best_word, best_score_tree = best_score_tree, works = works)
            if point > 0:
                imaginary_board = deepcopy(board)
                remove_word(best_word = current_word, best_score_tree = list_of_paths, board = imaginary_board)
                find_vowel_ratio(board = imaginary_board)
                check_connectivity(board = imaginary_board)
                if change_method == 0:
                    modified_score = (connectivity)*acc_point*((1/(0.0871*(2*math.pi)**0.5))*math.e**(-0.5*((vowel_ratio-0.395)/0.087)**2))
                    potentials.append([current_word, modified_score, acc_point, list_of_paths])
                else:
                    modified_score = (connectivity)*point*((1/(0.0871*(2*math.pi)**0.5))*math.e**(-0.5*((vowel_ratio-0.395)/0.087)**2))
                    potentials.append([current_word, modified_score, point, list_of_paths])
                if letters_left - len(current_word) in [1,2]:
                    potentials[found_word][1] *= 0.1
                found_word += 1
        print(len(potentials))
        potentials.sort(key=lambda s: s[1], reverse=True)
        try:
            x = potentials[0][2]
        except:
            board_finished = 1
        if board_finished == 0:
            if change_method == 0:
                print(potentials[0][0], potentials[0][2])
                final_score += potentials[0][2]
            else:
                print(potentials[0][0], potentials[0][2])
                final_score += potentials[0][2]
            points_p.append(final_score)
            letters_left -= len(potentials[0][0])
            letters_p.append(letters_left)
            imaginary_board = deepcopy(board)
            remove_word(best_word = potentials[0][0], best_score_tree = potentials[0][3], board = board)
    number_left_array.append([letters_left, final_score])
    print(final_score,"\n")
    board_finished = 0
print(final_score)
print(number_left_array)
