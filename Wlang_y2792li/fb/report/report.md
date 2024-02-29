# REPORT

## Personal Information
- Student Name: Yichu Li
- Student ID: 20817846
- WatID: y2792li

## What have been done to compile and run the code
I used docker to compile and run the fuzzing target, as the instructions showed in the readme file.

## What have been done to increase the coverage
I added two filename "~fuzz.wadt" to cover lines for w_wad.c. Also I covered some functions using code: 

```c
  D_PopEvent();
  DeviceIndex();
  LoadInstrumentTable();
  P_GroupLines();
  NetUpdate();
  D_StartGameLoop();
  PlayersInGame();
  D_QuitNetGame();
```

Then, the line coverage for w_wad.c and p_setup.c becomes 88.9 % and 82.3%. The total line coverage becomes 9.7%.

## What bugs have been found? Can you replay the bug with chocolate-doom, not with the fuzz target?
No, I don't find any bugs.

## Did you manage to compile the game and play it on your local machine (Not inside Docker)?
Yes, I did. I also provide a screeshot of playing the game.
