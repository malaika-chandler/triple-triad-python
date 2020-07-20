
# Triple Triad  
Triple Triad is a mini game within the PlayStation game Final Fantasy 8. This simple version that I've implemented so far uses the Random and Open rules by default. The elemental rule can be turned on or off.  

To keep my knowledge of python fresh, I implemented a basic version of one of my favorite games.  
  
## Getting Started  
  
### Prerequisites  
  
Requires Python 3.7+  
  
### Installing  
  
Download and unzip the project then enter the directory and run the game:  
  
```  
python triple_triad.py
```  
  
Or to start a game with the elemental rule  
  
```  
python triple_triad.py --elemental
```

## App Images

When a new game begins:  
![New Game](sample-images/game-beginning.png?raw=true "Game Start")

Player 1 starts by placing a card.  
![Player 1 Plays](sample-images/p1-placed-card.png?raw=true "Player 1 starts")

Player 2 responds by flipping Player 1's card. The cards in Player 2's possession will be displayed in their color.  
![Player 2 Responds](sample-images/p2-placed-card.png?raw=true "Player 2 responds")

The board after placing a card of a different element on an elemental space, demoting that card's ranks by 1.  
![Elemental Effect](sample-images/elemental-rule-effect.png?raw=true "How elemental rule affects cards")

The end game screen when the game ends in a draw.  
![End Game Display](sample-images/end-game-draw.png?raw=true "End game view for draw")
  
## Acknowledgments  
  
* Thanks to Square for creating Final Fantasy 8 and the game Triple Triad
* I implemented the opposition player using techniques I learned from working with Pacman AI projects were developed at UC Berkeley, primarily by John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
