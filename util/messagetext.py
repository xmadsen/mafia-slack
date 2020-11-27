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
