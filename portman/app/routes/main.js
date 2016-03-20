import Ember from 'ember';

function ajax(a) {
  return new Ember.RSVP.Promise(function(resolve, reject) {
    jQuery.ajax(a).fail(reject).success(resolve);
  });
}

function procWords(words) {
  return words.split('\n').filter(Boolean).uniq();
}

const MainRoute = Ember.Route.extend({
  model: function() {
    return Ember.Object.create({
      words1: '',
      words2: ''
    });
  },
  actions: {
    getPortmanteaus: function() {
      const controller = this.get('controller');
      const w1 = procWords(controller.get('model.words1'));
      const w2 = procWords(controller.get('model.words2'));
      const payload = JSON.stringify({ words1: w1, words2: w2 });
      ajax({
        type: 'POST',
        url: '/portmanteaus',
        dataType: 'json',
        contentType: 'application/json',
        data: payload,
      }).then(function(result) {
        controller.set('model.portmanteaus', result.portmanteaus);
      }).catch(function(err) {
        consoel.log(err);
      });;
    }
  }
});

export default MainRoute;
