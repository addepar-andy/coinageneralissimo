from flask import Flask, request, jsonify

import portmanatee

app = Flask('portman')

@app.route('/portmanteaus', methods=['POST'])
def portmanteaus():
    input = request.get_json()
    results = portmanatee.find_matches(input['words1'], input['words2'], thresh=0)
    results.sort(key=lambda t: t[2], reverse=True)
    results = [dict(w1=w1, w2=w2, score=score) for w1, w2, score in results]
    return jsonify(portmanteaus=results)

@app.route('/synset/<id>', methods=['GET'])
def synset(id):
    return jsonify(synset=ser_synset(portmanatee.synset(id)))

@app.route('/synset/<id>/hypos', methods=['GET'])
def synset_hypos(id):
    syns = portmanatee.synset(id).closure(lambda s:s.hyponyms(), depth=1)
    return jsonify(synsets=[ser_synset(s) for s in syns])

@app.route('/synset/<id>/hypers', methods=['GET'])
def synset_hyper(id):
    syns = portmanatee.synset(id).closure(lambda s:s.hypernyms(), depth=1)
    return jsonify(synsets=[ser_synset(s) for s in syns])

@app.route('/synset/<id>/rels', methods=['GET'])
def synset_rel(id):
    syns = portmanatee.synset(id).closure(lambda s:s.also_sees() + s.similar_tos(), depth=1)
    return jsonify(synsets=[ser_synset(s) for s in syns])

@app.route('/synsets/<wurd>', methods=['GET'])
def synsets(wurd):
    ser = [ser_synset(syn) for syn in portmanatee.synsets(wurd)]
    return jsonify(synsets=ser)

def ser_synset(syn):
    return {'id': syn.name(), 'def': syn.definition(), 'words': syn.lemma_names()}

if __name__ == '__main__':
    import sys
    print 'initializing... ',
    sys.stdout.flush()
    portmanatee.init()
    print 'done'
    app.run(debug=True)

