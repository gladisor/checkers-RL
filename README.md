# checkers-RL

## Description

This project is my attempt to create an AI that will be able to beat humans at the game of checkers.

## Equations

Error to be minimized is called temporal difference error (TDE).
Episodes are generated as followed: 
state, action, reward, Next state, next action ... until terminal state. The function 
q(S, A) is the value of taking action A in state S. The value of the previous state action pair gets updated to be closer to the next reward plus a discount factor gamma multiplied by the maximum action value of the next state.

![](images/td.png)

The Q function is optimized using backprop:

![](images/backprop.png)

## UML Diagrams

### Use Case Diagram
![](images/useDiagram.png)

### Class Diagram
![](images/classDiagram.png)

### Interaction Diagram
![](images/interactionDiagram.png)

## Authors
Tristan Shah

## Credits
Reinforcement Learning: 
	Ritchard S Sutton
	Andrew G Barto
## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details