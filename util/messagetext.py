from string import Template


class MessageText:
    KILLED_MAFIA = 'Justice prevails! A member of the mafia has been '\
        'rooted out.'
    KILLED_VILLAGER = 'In truth, they were no criminal. An innocent '\
        'villager has been killed.'

    MAFIA_WINS = 'The mafia has made an example of this village. No longer '\
        'will they resist the criminal empire.\nGAME OVER. The mafia wins.'
    VILLAGERS_WIN = 'The villagers have shown bravery and determination in '\
        'their resistance to organized crime. The mafia will think twice '\
        'before trying again.\nGAME OVER. The villagers win.'

    HOW_TO_VOTE = 'To vote guilty: ```/mafia vote-guilty```\nTo vote not '\
        'guilty: ```/mafia vote-innocent```'

    HOW_TO_ACCUSE = 'To accuse or second an accusation: ```/mafia accuse '\
        '@who-to-accuse```'

    ADD_PLAYER_SUCCESS = Template(
        ('<@${executor}> has joined the game! '
         '${num_players} players have joined!'
         )
    )
    ADD_PLAYER_ALREADY_IN = "You can't join if you're already in."
    ADD_PLAYER_GAME_ALREADY_STARTED = "The game has started. Maybe next time."
    ADD_PLAYER_FAILURE_GENERIC = "Something is wrong. You can't join the game."

    REMOVE_PLAYER_SUCCESS = Template('<@${executor}> has left the game!')
    REMOVE_PLAYER_FAILURE = "The game has started. You can't leave now!"

    START_GAME_SUCCESS = Template(
        ('The game is starting now! If you are in the mafia you '
         'will be notified...\n\nNight falls on the village. It is '
         'peaceful here, but not for long. The mafia is up to '
         'something.\n${message}'
         )
    )
    START_GAME_FAILURE = "The game can't start with less than 4 players!"

    MURDER_DAY = Template(
        ('Another beautiful morning! One that <@${target}> '
         'won\'t get to experience, for they are dead! Murdered in'
         ' the night! One among you is the culprit!\n'
         '${accuse_message}')
    )
    MURDER_GAMEOVER = Template(
        ('<@${target}> is found dead in the morning.\n'
         '${gameover_message}')
    )
    MURDER_FAILED = 'Hit attempt failed. Either this person does not exist or'\
        ' they are a member of the mafia and are under protection.'\
        ' Make sure you are tagging your target with @.'

    ACCUSE_SECONDED = Template(
        ('The charge against <@${target}> has been seconded by '
         '<@${executor}>. In accordance with the village by-laws they'
         'now stand before a jury of their peers. The penalty for'
         'guilt is... DEATH. Will you vote guilty or not guilty?\n'
         '${howtovotemessage}')
    )
    ACCUSE_FIRSTTIME = Template(
        ('<@${target}> has been formally accused of being a member'
         ' of the mafia by <@${executor}>. This is a serious '
         'accusation and before they stand trial it must be'
         ' seconded!\n${howtoaccusemessage}')
    )
    ACCUSE_INVALID = 'Sorry that is not a valid target.'

    VOTE = Template('<@${executor}> casts their ballot. ${action}!')
    VOTED_GUILTY = Template(
        ('<@${guilty}> has been found guilty. ${killedmessage} They swing '
         'from the gallows as night falls on the village.\n${roster}'
         )
    )
    VOTED_GUILTY_GAMEOVER = Template(
        ('<@${guilty}> has been found guilty. ${killedmessage} '
         '${gameovermessage}'
         )
    )

    VOTED_INNOCENT = Template(
        ('<@${innocent}> has mounted a successful defense and been found not'
         ' guilty. Someone\'s gonna hang before the day is through. The '
         'question is who?')
    )
