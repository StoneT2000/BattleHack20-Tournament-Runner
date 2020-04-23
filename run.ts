import * as Dimension from './src';
import fs from 'fs';
import DummyDesignClass from './src/dummyDesign';
let Match = Dimension.Match;
let RANK_SYSTEM = Dimension.Tournament.RANK_SYSTEM

// the framework was intended to use something else and requires this design thing, ignore this part
let DummyDesign = new DummyDesignClass('Battle Hack!', {
});
let myDimension = Dimension.create(DummyDesign, {
  name: 'Battle Hack 2020',
  loggingLevel: Dimension.Logger.LEVEL.WARN,
});

if (!fs.existsSync('./replays')){
  fs.mkdirSync('./replays');
}

/** Make your edits here */

// load your bots and their names by passing in a path to the bot directory and giving a name as an object
let botList = [];
botList.push({file: './examplefuncsplayer', name:'Example 1'});
for (let i = 2; i <= 16; i++) {
  botList.push({file: './examplefuncsplayer', name:'Example ' + i});
}

// create the tournament
let BattlehackTourney = <Dimension.Tournament.Ladder.Tournament>(myDimension.createTournament(botList, {
    type: Dimension.Tournament.TOURNAMENT_TYPE.LADDER,
    rankSystem: RANK_SYSTEM.TRUESKILL, // change to RANK_SYSTEM.ELO for elo rankings
    loggingLevel: Dimension.Logger.LEVEL.ERROR,
    name: 'BattleHack 2020 Trueskill Tournament',
    consoleDisplay: true,
    defaultMatchConfigs: {
      boardsize: 16,
      maxrounds: 500,
      loggingLevel: Dimension.Logger.LEVEL.NONE
    },
    agentsPerMatch: [2],
    tournamentConfigs: {
       // max concurrent matches
      maxConcurrentMatches: 4,
      // max matches to play in the tournament. Remove if you don't want it to be capped
      maxTotalMatches: 1000
    },
    resultHandler: (result) => result
  }
));

// run the tournament
BattlehackTourney.run();