# a2-release-res
Problem 1:

PROBLEM UNDERSTANDING:
Minimax algorithm can be used to solve the given adversarial search problem. Two players alternate turns in a fully visible zero sum game. The player who
begins the game first is known as the "max" player and will choose the move with the highest utility value from a range of options. The "min" player
is the one who comes out second. The "min" player will pick the option with the lowest utility value among the available options. In doing so, each
player is playing to his or her own advantage while doing the least amount for the other player.

ABSTRACT:
Initial state: a random position on the board from which the maximum number of players will move.
State space:  all possible configurations of the board
Successor function: all possible board configurations that comply with the rules for movements with the current state.
Terminal state: State where one player won which corresponds to only single colour pieces remaining on the board.
Cost: Although edge points are assumed to be uniform, the best move is determined by comparing each state's favorability to the maximum player to
other potential states.

Algorithms used: Minimax and Alpha-Beta Pruning
To choose the next action that will result in the best possible result, Minimax uses depth first search. The game's branching feature determines
how far the search can go. The branching factor (successors created by a given state) in this situation may be as high as 40. Therefore, it is not
practical to search a comprehensive game tree that contains all potential terminal states. Instead, the technique can be used in a depth-limited
search to provide an ideal move that only considers a few movements in the future. A value is assigned to each leaf node of the game tree at a given
horizon depending on how likely it is for the maximum player to win the game from that state. The min and max nodes, which stand for the'max'
player selecting the highest value and the'min' player selecting the lowest value, respectively, symbolize the players who choose those values as
they are propagated back up the tree. A strong positive value for a state that is advantageous to the "max" player, a strong negative number for
a state that is advantageous to the "min" player, and 0 for a neutral board should make up the evaluation function.
Alpha-beta pruning is a technique that can be used to boost the effectiveness of a search to a specific horizon in addition to limiting the depth
of the search. Searching nodes that have no impact on the best option are removed through alpha-beta pruning. The search below a node that won't ever
 be selected is stopped. This enables a deeper tree to be searched or the best search to be returned more quickly.

PROGRAM IMPLEMENTATION:
For a given player and board setup:
The player is assigned to max player.

A terminal state is one in which the "max" player wins, therefore find all of the max player's potential future movements and check if any of them
are terminal situations. Reverse that move if applicable. Add a depth layer to the game tree and scan two moves in advance if there are no winning
moves left. For every leaf node, compute the evaluation function. The maximum value of the leaf nodes should be propagated up to each of their
parent nodes since they are the children of a max node. Afterward, propagate up to each parent node's minimum value from the values of the next
depth layer. Pick the best move for the maximum player by selecting the maximum of these propagated values.

As previously mentioned, the high branching factor and constrained length of time to devise a move need either exhaustively searching a tree with
a short horizon or using an alpha-beta pruning to enable searching a deeper tree. The likelihood that the best option provided would result in a
win for the "max" player increased as the search depth increased. The creation of the evaluation function is a possibility for enhancing performance
in game play, however, following attempts at implementing alpha-beta pruning have failed.
Evaluation function has three parts given as follows:
---->Pichus, pikachus, and raichus are weighted 1, 2, and 10 respectively.  We calculate the difference between the weighted sum of these pieces.
---->We calculate the difference of jump moves available for each player.
---->We calculate the difference of the mean of the squared distance traveled by pichus and pikachus.
These three parameters are then weighted based on the current condition of the board after seeing the game being played against the random AI and
the AIs of other students.
---->The weighted sum of pieces differential is initially given a slight advantage when there are no raichus on the board, then pichus and pikachus
are advanced down the board to transform into raichus.
---->Once a player possesses a raichu, taking opponent pieces takes precedence over all other considerations.
---->Priority is given to advancing pichus/pikachus to turn into raichus if there is a high differential between weight sum of pieces (max player
is the equivalent of over 2 raichus ahead).
---->Lastly, the goal is yet again on capturing opponent pieces in an effort to win the game if the "max" player is 3 raichus ahead.
---->The evaluation function mentioned above was able to provide moves that could win or play to a draw against other AI players despite the search tree's narrow horizon.


Problem 2:

PROBLEM UNDERSTANDING:
    For this problem we are given a dataset which consists of sentences which are basically user generated hotel reviews. These reviews are labelled
into two classes "truthful" and "deceptive". Our task is to use Naive Bayes Classifier and to train the dataset and store the calculations
from the training phase. And based on these calculations classify the reviews in the test dataset accordingly.

CODE IMPLEMENTATION:
To implement the given problem, we first declare an empty dictionary called 'occurrences_dict'. This dictionary is used to store the count of all the
unique words that are present in the dataset. We then traverse in the train_data["objects"] which is a list of strings corresponding to reviews. We
preprocessed the reviews in order to clean the data by using strip(), split() and lower(). We have also created a function called 'remove_punc' which
will filter out the punctuation marks from the reviews. We are traversing through each word in the cleaned data and for each new word that we encounter, we keep
adding it to the 'occurrences_dict'. Train_data["labels"] is a list of strings corresponding to ground truth labels for each review. For each word
present, in the 'occurrences_dict', we check the truth label for that word in the train data. According to its truth label, we add the count of
occurrences to its respective class.
Similarly, we carry out the same preprocessing steps for the test data. For every term in cleaned_pt if the term not in occurrences_dict continue.
Else if deceptive or truthful not in occurrences_dict, continue. We defined a truth_deceptive ratio which has been initialised to 1. For each word
encountered in the test data, we calculate the ratio as follows:-
            truth_decep_ratio = truth_decep_ratio * occurrences_dict[individual_word]['truthful'] / occurrences_dict[individual_word]['deceptive'].
So, if the ratio is greater than 1 we are appending 'truthful' to the final_list or else we are appending 'deceptive' to the final_list. We then return
the final_list. Lastly, we calculate the accuracy obtained by our Naive-Bayes assumption on the Bayesian classifier.

OBSERVATIONS AND INFERENCES:
On running the code as is, we observed an accuracy of 50% due to equal number of reviews in both the classes. Thus, our aim was to get a decent accuracy
above 50% atleast. We finally obtained an accuracy of 83.50% after implementing Naive-Bayes assumption on the Baysian classifier.
