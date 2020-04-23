import * as Dimension from './src';

export default class DummyDesignClass extends Dimension.Design {
  async initialize() {

  }
  async update() {
    return Dimension.Match.Status.RUNNING;
  }
  async getResults() {

  }

}