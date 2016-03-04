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
    lucky: function() {
      const ids = [];
      this.get('synGroups').forEach((syns) => {
        syns.forEach((syn) => {
          ids.push(syn.get('id'));
        });
      });
      const payload = JSON.stringify({synset_ids: ids.uniq()});
      ajax({
        type: 'POST',
        url: '/gimme',
        dataType: 'json',
        contentType: 'application/json',
        data: payload,
      }).then((result) => {
        const myWords = result.words.join('\n')
        this.set('target', this.get('target') + '\n' + myWords);
      })
    },
    search: function() {
      const wurd = this.get('searchStr');
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
