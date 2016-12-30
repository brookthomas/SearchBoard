class Recommender {

  termPreprocessor (terms_from_input) {
    let terms = terms_from_input.split(new RegExp("[^a-zA-Z0-9]")).filter( (term) => term.length );        // Split
    terms.forEach(function (term,i,terms) { terms[i] = term.toLowerCase(); });                             // Lowercase
    terms.forEach(function (term,i,terms) { terms[i] = stemmer(term); });                                  // Stem
    terms = terms.filter( (term) => term in positional_index);
    return terms;
  }

  getEligibleDocuments(terms) {
    let docs = [];
    // Get all eligible documents
    terms.forEach(function (term) {
      if (positional_index[term]) {
        for (let doc of Object.keys(positional_index[term])) {
          if (!docs.includes(doc)) { docs.push(doc); }
        }
      }
    });
    return docs;
  }

  getDocumentScore(id, terms) {
    let total = 0;
    let scores = terms.map( (term) => this.getDocumentTermScore( id, term ) ).filter( (score) => score );
    scores.forEach( (term_stats) => total += term_stats.bm25 * term_stats.sent );

    return {'id':id, 'score': total.toFixed(3), 'terms': scores }
  }

  getDocumentTermScore(doc,term) {
    if (!positional_index[term].hasOwnProperty(doc)) { return undefined; }

    return { 
        term:term, 
        bm25: this.getBM25( doc, term ).toFixed(3),
        sent: this.getAverageSentiment( doc, term ).toFixed(3),
        excerpt: this.getTopSentenceBySentiment( doc,term ).replace(new RegExp(term, 'i'), `<span class='highlight'>${term}</span>`)
    }
  }

  getBM25(doc,term) {
    return (doc in bm25[term]) ? bm25[term][doc] : 0;
  }

  getAverageSentiment(doc,term) {
    if (!(doc in positional_index[term])) { return 0; }
    
    let sum = 0;
    for (let pos of positional_index[term][doc]) {
      sum += this.getSentiment(doc, pos);
    }
    return sum / positional_index[term][doc].length;
  }

  getSentiment(doc, position) {
    return sentiment[doc][position];
  }

  getTopSentenceBySentiment( doc, term ) {
    return positional_index[term][doc]
      .map( ( pos ) => ({ 'pos': pos, 'excerpt': sentences[doc][pos], 'score': this.getSentiment( doc, pos ) }) ) 
      .sort( ( a, b ) => (a > b) ? 1 : -1 )[0].excerpt;
  }


  run(terms_from_input) {
    let results_view = $('.results').html('');
    let terms = this.termPreprocessor(terms_from_input);
    let documents = this.getEligibleDocuments(terms, positional_index);
    let results = documents.map( (doc) => this.getDocumentScore(doc, terms));

    if ( results.length == 0 ) {
      $('.results').append($('<div>').text('No results found.').animate({opacity:'-=1'},1200));
    } else {
      for (let r of results.sort(function (score_a, score_b) { return (score_a.score < score_b.score) ? 1 : -1; }).slice(0,6)) {
        $('.results').append(Handlebars.templates.game_card({ title: games[r.id], image: `assets/${r.id}.jpg`, score: r.score, excerpts: r.terms }));;
      }
    }
  }

}