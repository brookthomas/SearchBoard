(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['game_card'] = template({"1":function(container,depth0,helpers,partials,data) {
    var stack1, helper, alias1=depth0 != null ? depth0 : {}, alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression;

  return "    <div class='mdl-card__actions mdl-card--border'>\n      <span class='excerpt'>\""
    + ((stack1 = ((helper = (helper = helpers.excerpt || (depth0 != null ? depth0.excerpt : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"excerpt","hash":{},"data":data}) : helper))) != null ? stack1 : "")
    + "\"</span>\n      <div class='metrics'>\n        <span><span class='metric-title'>BM25</span>"
    + alias4(((helper = (helper = helpers.bm25 || (depth0 != null ? depth0.bm25 : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"bm25","hash":{},"data":data}) : helper)))
    + "</span>\n        <span><span class='metric-title'>SENT</span>"
    + alias4(((helper = (helper = helpers.sent || (depth0 != null ? depth0.sent : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"sent","hash":{},"data":data}) : helper)))
    + "</span>\n      </div>\n    </div>\n";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1, helper, alias1=depth0 != null ? depth0 : {}, alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression;

  return "<div class='game-card mdl-card mdl-shadow--2dp'>\n  <div class='mdl-card__title mdl-card--expand' style='background: url(\"assets/game.jpg\") center center no-repeat; background-size: cover;'>\n  </div>\n  <div class='mdl-card__supporting-text'>\n    <span class='title'>"
    + alias4(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"title","hash":{},"data":data}) : helper)))
    + "</span>\n    <span class='score'>"
    + alias4(((helper = (helper = helpers.score || (depth0 != null ? depth0.score : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"score","hash":{},"data":data}) : helper)))
    + "</span>\n  </div>\n"
    + ((stack1 = helpers.each.call(alias1,(depth0 != null ? depth0.excerpts : depth0),{"name":"each","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "")
    + "</div>\n\n";
},"useData":true});
})();