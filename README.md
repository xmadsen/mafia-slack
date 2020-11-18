# mafia-slack
[![Add To Slack](https://platform.slack-edge.com/img/add_to_slack.png)](https://slack.com/oauth/v2/authorize?scope=chat:write,commands,groups:write,groups:read&client_id=295285222965.1231423698087&redirect_uri=https://p6ew7pnsna.execute-api.us-east-1.amazonaws.com/Prod/addtoslackredirect)
## Dev Guide
### Install dependencies
```
pip install -r .\requirements-dev.txt
```
### Run Tests
```
python -m pytest
```
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
    - [x] main channel notified of state
- Trial
  - [x] GUILTY - If majority of players vote guilty, the accused is killed and state transitions to Night.
  - [x] NOT_GUILTY - If majority of players vote not guilty, the accused is acquitted and state transitions back to Day.
  - [x] Channel notifications
- Game Over