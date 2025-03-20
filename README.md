# Chess-engine-with-minimax

1 Objective

In this assignment, you will develop a computer vs human chess game using
pygame for visualization and python-chess for move validation. You will im-
plement an AI opponent using the Minimax algorithm with a limited depth
and an evaluation function to assess board positions. Finally, you will write
a report analyzing the impact of search depth and evaluation functions on AI
performance.

2 Requirements

2.1 Game Implementation

• Use pygame to render a chessboard and display the pieces.
• Allow a human player (White) to make legal moves by clicking squares.
• Implement an AI opponent (Black) using the Minimax algorithm with a
limited depth.
• Use python-chess to determine valid moves and apply them.
• Detect checkmate, stalemate, or draw conditions and display a message.

2.2 Minimax AI

• Implement Minimax with a limited search depth.
• Create an evaluation function (e.g., material count).

2.3 Report

• Explain how python-chess was used for move validation.
• Discuss the Minimax algorithm, the evaluation function, and move ordering.
• Analyze how increasing/decreasing depth affects AI strength and perfor-
mance.
• Analyze the impact of pruning on the efficiency of AI performance and the
selection of moves.
• Include experiments where the AI plays against itself at different depths.

3 Submission

Submit the following files:
• Python code implementing the game.
• Report analyzing AI behavior with different depths and evaluation functions.

4 Resources

• python-chess documentation
• Pygame documentation
• Minimax algorithm
