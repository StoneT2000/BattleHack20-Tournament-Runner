import * as Dimension from './src';
import DummyDesignClass from './src/dummyDesign';
let Match = Dimension.Match;

// the framework was intended to use something else and requires this design thing, ignore this part
let DummyDesign = new DummyDesignClass('Battle Hack!', {
});
let myDimension = Dimension.create(DummyDesign, {
  name: 'Battle Hack 2020',
  loggingLevel: Dimension.Logger.LEVEL.WARN,
}); 

// load your bots and their names
let botList = [];
botList.push({file: './examplefuncsplayer', name:'Example 1'});
botList.push({file: './examplefuncsplayer', name:'Example 2'});

let BattlehackTourney = <Dimension.Tournament.Ladder.Tournament>(myDimension.createTournament(botList, {
    type: Dimension.Tournament.TOURNAMENT_TYPE.LADDER,
    rankSystem: Dimension.Tournament.RANK_SYSTEM.TRUESKILL,
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
      maxConcurrentMatches: 1,
      // max matches
      maxTotalMatches: 1000
    },
    resultHandler: (result) => result
  }
));

BattlehackTourney.run();