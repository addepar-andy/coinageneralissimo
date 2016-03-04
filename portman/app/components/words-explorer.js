import Ember from 'ember';

function ajax(a) {
  return new Ember.RSVP.Promise(function(resolve, reject) {
    jQuery.ajax(a).fail(reject).success(resolve);
  });
}

export default Ember.Component.extend({
  searchStr: '',
  synGroups: Ember.computed(function() { return Ember.A(); }),

  actions: {
    clear: function() {
      this.set('synGroups', Ember.A());
    },
    search: function(wurd) {
      ajax({
        url: '/synsets/' + wurd.trim()
      }).then((results) => {
        const syns = Ember.A(results.synsets.map(s => Ember.Object.create(s)));
        this.get('synGroups').addObject(syns);
      }).catch(function(err) {
        console.log(err);
      });
    },
    hide: function(grp) {
      this.get('synGroups').removeObject(grp);
    },
    add: function(grp) {
      for (var i = 0; i < grp.length; i++) {
        const synset = grp[i];

        const myWords = synset.get('words').join('\n');
        this.set('target', this.get('target') + '\n' + myWords);
      }
    }
  }
});
