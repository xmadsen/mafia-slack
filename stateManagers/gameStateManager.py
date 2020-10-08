import random
from models.gameState import States as GameStates
from models.player import Player, Roles, States as PlayerStates

class Actions:
    START_GAME = 'START_GAME'
    ACCUSE = 'ACCUSE'
    MURDER = 'MURDER'
    GUILTY = 'GUILTY'
    NOT_GUILTY = 'NOT_GUILTY'

    ADD_PLAYER = 'ADD_PLAYER'
    REMOVE_PLAYER = 'REMOVE_PLAYER'

class GameStateManager(object):
    
    def __init__(self, gameState):
        self.gameState = gameState

    def transition(self, action, data=None, executor=None):
        '''
            data - typically the player id of the player who the action is targeting
            executor - the player id of the player who is taking the action.
        '''
        print(f'state {self.gameState.state} - {action} - {data} - {executor}')
        oldState = self.gameState.state
        ret = False
        if self.gameState.state == GameStates.MARSHALLING:
            ret = self._transitionFromMarshalling(action, data, executor)
        elif self.gameState.state == GameStates.NIGHT:
            ret = self._transitionFromNight(action, data, executor)
        elif self.gameState.state == GameStates.DAY:
            ret = self._transitionFromDay(action, data, executor)
        elif self.gameState.state == GameStates.TRIAL:
            ret = self._transitionFromTrial(action, data, executor)
        
        if self.gameState.state != oldState:
            #reset player votes
            for p in self.gameState.players:
                p.vote=None
        return ret
    def _transitionFromMarshalling(self, action, data, executor):
        if action == Actions.START_GAME:
            if len(self.gameState.players) >= 4:
                self._assignPlayerRoles()
                self.gameState.state = GameStates.NIGHT
                return True
        elif action == Actions.ADD_PLAYER:
            p = Player(executor)
            if self.gameState.findPlayerWithId(executor) == None:
                self.gameState.players.append(p)
                return True
        elif action == Actions.REMOVE_PLAYER:
            toRemove = self.gameState.findPlayerWithId(executor)
            self.gameState.players.remove(toRemove)
            return True
        return False

    def _transitionFromNight(self, action, data, executor):
        if action == Actions.MURDER:
            toMurder = self.gameState.findPlayerWithId(data)
            if toMurder == None or toMurder.role == Roles.MAFIA:
                return False
            murderer = self.gameState.findPlayerWithId(executor)
            if murderer.role != Roles.MAFIA:
                return False
            murderer.vote = toMurder.id
            mafiaMembers = self.gameState.findPlayersWithRole(Roles.MAFIA)
            livingMafia = [m for m in mafiaMembers if m.state == PlayerStates.ALIVE]
            if len([m for m in mafiaMembers if m.vote == toMurder.id]) == len(livingMafia):
                toMurder.state = PlayerStates.DEAD
                if self._isGameOver():
                    self.gameState.state = GameStates.GAME_OVER
                else:
                    self.gameState.state = GameStates.DAY
            return True
        return False

    def _transitionFromDay(self, action, data, executor):
        if action == Actions.ACCUSE:
            accusedPlayer = self.gameState.findPlayerWithId(data)
            accuser = self.gameState.findPlayerWithId(executor)
            if accusedPlayer and accuser and accusedPlayer.state == PlayerStates.ALIVE and accuser.state == PlayerStates.ALIVE:
                accuser.vote = accusedPlayer.id
                if self.gameState.voteCount(accusedPlayer.id) >= 2:
                    accusedPlayer.state = PlayerStates.ON_TRIAL
                    self.gameState.state = GameStates.TRIAL
                    self.gameState.last_accused = accusedPlayer.id
                return True
        return False

    def _transitionFromTrial(self, action, data, executor):
        accused = self.gameState.findPlayerOnTrial()
        juror = self.gameState.findPlayerWithId(executor)
        ret = False
        if accused and juror and juror.can_vote():
            if action == Actions.NOT_GUILTY or action == Actions.GUILTY:
                juror.vote = action
                ret = True
            self._checkTrialState(accused)
        return ret

    def _checkTrialState(self, accused):
        jury_count = len([p for p in self.gameState.players if p.can_vote()])
        votes_to_acquit = self.gameState.voteCount(Actions.NOT_GUILTY) #len([p for p in self.gameState.players if p.can_vote() and p.vote == Actions.NOT_GUILTY])
        votes_to_convict = self.gameState.voteCount(Actions.GUILTY) #len([p for p in self.gameState.players if p.can_vote() and p.vote == Actions.GUILTY])
        print(f'{jury_count} members on the jury')
        print(f'{votes_to_acquit} votes to acquit')
        print(f'{votes_to_convict} votes to convict')
        if votes_to_acquit + votes_to_convict == jury_count:
            if votes_to_acquit >= votes_to_convict:
                accused.state=PlayerStates.ALIVE
                self.gameState.state = GameStates.DAY
            else:
                accused.state = PlayerStates.DEAD
                if self._isGameOver():
                    self.gameState.state = GameStates.GAME_OVER
                else:
                    self.gameState.state = GameStates.NIGHT

    def _assignPlayerRoles(self):
        numMafia = self._getMafiaCount()
        shuffledRoster = random.sample(self.gameState.players,len(self.gameState.players))
        for p in shuffledRoster[:numMafia]:
            p.role = Roles.MAFIA
        for p in shuffledRoster[numMafia:]:
            p.role = Roles.VILLAGER
    
    def _getMafiaCount(self):
        return  len(self.gameState.players) // 3

    def _isGameOver(self):
        mafiaCount = len([p for p in self.gameState.findPlayersWithRole(Roles.MAFIA) if p.state == PlayerStates.ALIVE])
        villagerCount = len([p for p in self.gameState.findPlayersWithRole(Roles.VILLAGER) if p.state == PlayerStates.ALIVE])
        
        return mafiaCount == 0 or villagerCount == mafiaCount

    def printGameState(self):
        playerList = sorted(self.gameState.players,key=lambda player: player.role)
        print('ROSTER:')
        print('id|role|state')
        for p in playerList:
            print(p)
        print(f'GAME STATE: {self.gameState.state}')