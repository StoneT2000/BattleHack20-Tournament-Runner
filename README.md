# BattleHack 2020 Tournament Runner

This is code for running your own Trueskill / ELO ranked tournament with bots from BattleHack 2020 hosted by [Battlecode](https://battlecode.org)

This is essentially my [Dimensions](https://battlecode.org) framework wrapped around Battlecode.

To start, make sure you have [npm](https://npmjs.org) and run the following

```
npm install
```

Make sure to install `ts-node` by running the following

```
npm install -g ts-node
```

Then to start running a tournament, run
```
ts-node run.ts
```

This will run 16 examplefuncsplayer against themselves in a trueskill tournament with 4 matches running simutaneously. Replays are automatically stored in the `replays/` folder.

To run with other bots, read through `run.ts` for instructions.
