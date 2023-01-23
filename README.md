# wordsoup
Word Soup Project

PROJECT DESCRIPTION:

Word Soup is a word game that involves selecting words on a jumbled grid of letters, and attempting
to achieve a high score by choosing long words with uncommon letters and clearing the board. This
project sets out to create a heuristic algorithm that can beat humans in the game Word Soup. By
creating a simulated version of the game in Python and creating a depth-first search that could
locate words and remove them from the board, I created a greedy algorithm that would select the
one-turn optimal word every turn. The greedy algorithm consistently beat the amateur player, but
the expert player was still scoring higher by clearing the board consistently. Then, I analyzed the
differences in how the game was played by the expert player and the greedy algorithm, and looked
at what heuristics could be used to improve on the greedy algorithm. After adding 3 different
heuristics to the greedy algorithm which considered the composition of letters left on the board after
each turn, the average score improved and the average number of letters left on the board halved
in comparison to the greedy algorithm. This also marked a narrowing of the gap in performance
between the algorithm and the expert player, both in score and amount of board cleared.

CODE USAGE:

The code should run as is, provided the accompanying text file 'altered_points_2' is in the same directory.
