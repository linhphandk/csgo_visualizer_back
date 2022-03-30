# csgo_visualizer_back

# Data extraction
## Common entities
### Data format
Every entry of a match has the date time appended to it in the format of `MM/DD/YYYY - HH:MM:SS:` an example would be 11/28/2021 - 20:33:34: therefore the regular expression is `\d+\/\d+\/\d+ - \d+:\d+:\d+:`

### Player tag
The players are identified with their player name, game id, steam id and the team they are assigned to.

When a player connects to a game his initial steam id is BOT or a steam id fx. STEAM_1:1:17960540

Players in the game can be assigned to:
- Unassigned - The player is not part of a team
- Spectator - used for users that are in charge of spectating
the game (GOTV)
- CT - Counter terrorists
- TERRORIST - terrorists

Examples:
- `electronic<20><BOT><Unassigned>` - player electronic without a steam id and without a team
- `ZywOo<26><STEAM_1:1:76700232><CT>` - player ZywOo in the team CT

In general we are interested only in players that are assigned to the CT or TERRORIST therefore the player tags would match `"\w+<\d+><.+><(CT|TERRORIST)>"`

### Player position 

The player position is defined by three numbers [x, y ,z] where the number can also be negative therefore this regex will match `\[-?\d+ -?\d+ -?\d+\]`

### Game/Round start
The main game is triggered by the Match_start log, but that also applies to the warmup rounds before the main game. The game is played on the FACEIT server (lets not play on 64 tick) so the actual match starts after the ` [FACEIT^] LIVE!` live (note that there is a extra space and end-of-transmittion character) after that there is a World start event and then a match start later followed by a round end so in practice it would look like:

1. `11/28/2021 - 20:41:09:  [FACEIT^] LIVE!`
2. `11/28/2021 - 20:41:31: World triggered "Round_Start"`
3. `11/28/2021 - 20:43:11: World triggered "Round_End"`

## Kills
The data entry of a kill have a format of 
`"misutaaa<24><STEAM_1:1:60631591><CT>" [594 625 -479] killed "Perfecto<28><STEAM_1:0:80477379><TERRORIST>" [113 -151 -352] with "m4a1_silencer"`

Where you have the attached player tag, position, the killed verb, the killed player tag, the with word and the item used to kill the person therefore we would use the combinations of player tags and the position.

so our regular expression would be:

`player tag position killed player tag position with \"\w+\" \(headshot\)`

## Attacks
Attack are the same as kills but you add also the damage dealt and current status of health and armor and where the person was attacked

