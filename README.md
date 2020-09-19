# mafia-slack
## Game State Machine
### States and actions
- Marshalling
  - [x] ADD_PLAYER
  - [x] REMOVE_PLAYER
  - [x] START_GAME - Transitions state to Night if enough players have joined.
    - [x] player roles assigned at random.
    - [x] mafia players assigned to a private channel.
- Night
  - [x] MURDER - The mafia kills a villager and transitions state to day.
- Day
  - [ ] ACCUSE - A player accuses another of being in the mafia. state transitions to Trial
- Trial
  - [ ] GUILTY - If majority of players vote guilty, the accused is killed and state transitions to Night.
  - [ ] NOT_GUILTY - If majority of players vote not guilty, the accused is acquitted and state transitions back to Day.
- Game Over