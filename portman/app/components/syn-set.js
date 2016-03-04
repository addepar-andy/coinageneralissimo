import Ember from 'ember';

function ajax(a) {
  return new Ember.RSVP.Promise(function(resolve, reject) {
    jQuery.ajax(a).fail(reject).success(resolve);
  });
}

function addWords(synset, which) {
}

export default Ember.Component.extend({
  classNames: ['syn'],
  synset: null,
  showDef: true,
  wordsTarget: null,
  explorerSyns: null,
  myGroup: null,

  findMore: function(which) {
    const id = this.get('synset.id');
    ajax({
      url: '/synset/' + id + '/' + which
    }).then((results) => {
      const syns = Ember.A(results.synsets.map(s => Ember.Object.create(s)));
      this.get('explorerSyns').addObject(syns);
    })
  },

  actions: {
    add: function() {
      const myWords = this.get('synset.words').join('\n');
      const words = this.get('wordsTarget');
      this.set('wordsTarget', words + '\n' + myWords);
    },
    up: function() {
      this.findMore('hypers');
    },
    down: function() {
      this.findMore('hypos');
    },
    rel: function() {
      this.findMore('rels');
    },
    hide: function() {
      this.get('myGroup').removeObject(this.get('synset'));
    }
  }
});
