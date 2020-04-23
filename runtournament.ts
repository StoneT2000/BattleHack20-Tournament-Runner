import * as Dimension from './src';
let Match = Dimension.Match;
import DummyDesignClass from './dummyDesign';

// the framework was intended to use something else and requires this design thing, ignore this part
let DummyDesign = new DummyDesignClass('Battle Hack!', {
});
let myDimension = Dimension.create(DummyDesign, {
  name: 'Battle Hack 2020',
  loggingLevel: Dimension.Logger.LEVEL.WARN,
}); 

let botList = [];
// botList.push({file: './bots/bishop', name:'Bishop'});
// botList.push({file: './bots/pawn', name:'Pawn'});
// botList.push({file: './bots/rook', name:'Rook'});
// botList.push({file: './bots/knight', name:'Knight'});
botList.push({file: './bots/thequeen3v3', name:'Queen - Stone'});
botList.push({file: './bots/syncbotv2', name:'Syncbot IDIOOT'});

let BattlehackTourney = <Dimension.Tournament.Ladder.Tournament>(myDimension.createTournament(botList, {
    type: Dimension.Tournament.TOURNAMENT_TYPE.LADDER,
    rankSystem: Dimension.Tournament.RANK_SYSTEM.TRUESKILL,
    loggingLevel: Dimension.Logger.LEVEL.ERROR,
    name: 'BattleHack 2020 Trueskill Tournament',
    consoleDisplay: true,
    defaultMatchConfigs: {
      // explanatory
      boardsize: 16,
      maxrounds: 500,
      loggingLevel: Dimension.Logger.LEVEL.NONE
    },
    agentsPerMatch: [2],
    tournamentConfigs: {
    },
    resultHandler: (result) => result
  }
));

BattlehackTourney.setConfigs({
  tournamentConfigs: {
    // max concurrent matches
    maxConcurrentMatches: 1,
    // max matches
    maxTotalMatches: 1000
  }
});

BattlehackTourney.run();