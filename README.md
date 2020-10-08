# mafia-slack
![Build Status](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiR2JPVk1vbEZ6aXFSM2JYSGpUcGF5TzVxQytUbHFjSnc3N3JrY2U3K2Y5NVpKNlBqRENPUDhXRXlGelhVdkJZL2lmTVNTd2FVU0prRjZCVmkzTTNMYmtJPSIsIml2UGFyYW1ldGVyU3BlYyI6Im14T20wWksxaTVTdUtlRTQiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)
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
    - [x] villager state is DEAD
    - [x] main channel notified of the state
- Day
  - [x] ACCUSE - A player accuses another of being in the mafia. state transitions to Trial
    - [ ] main channel notified of state
- Trial
  - [x] GUILTY - If majority of players vote guilty, the accused is killed and state transitions to Night.
  - [x] NOT_GUILTY - If majority of players vote not guilty, the accused is acquitted and state transitions back to Day.
  - [ ] Channel notifications
- Game Over