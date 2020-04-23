import * as Dimension from './src';
let Match = Dimension.Match;
const DummyDesignClass = require('./rps').RockPaperScissorsDesign;

// the framework was intended to use something else and requires this design thing, ignore this part
let DummyDesign = new DummyDesignClass('Battle Hack!', {
});
let myDimension = Dimension.create(DummyDesign, {
  name: 'Battle Hack 2020',
  loggingLevel: Dimension.Logger.LEVEL.WARN,
}); 

let botList = [];
botList.push({file: './bots/bishop', name:'Bishop'});
botList.push({file: './bots/pawn', name:'Pawn'});
botList.push({file: './bots/rook', name:'Rook'});
botList.push({file: './bots/knight', name:'Knight'});
botList.push({file: './bots/thequeen3v3', name:'Queen v3'});
botList.push({file: './exampleFuncsPlayer', name:'exampleFuncsPlayer'});

let BattlehackTourney = <Dimension.Tournament.Ladder.Tournament>(myDimension.createTournament(botList, {
    type: Dimension.Tournament.TOURNAMENT_TYPE.LADDER,
    rankSystem: Dimension.Tournament.RANK_SYSTEM.TRUESKILL,
    loggingLevel: Dimension.Logger.LEVEL.ERROR,
    name: 'Battlehack Trueskill Tournament',
    consoleDisplay: true,
    defaultMatchConfigs: {
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
    maxConcurrentMatches: 2,
    maxTotalMatches: 4
  }
});

BattlehackTourney.run();