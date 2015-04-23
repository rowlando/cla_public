'use strict';

var util = require('util');

exports.command = function(fields, value, callback) {
  var client = this;

  this.perform(function() {
    client.clickOption = function(field, value) {
      var el = util.format('input[name="%s"][value="%s"]', field, value);
      client.isVisible(el, function(result) {
        if(result.value === true) {
          client.click(el);
        }
      });
    };

    if(fields.constructor === Array) {
      fields.forEach(function(field) {
        client.clickOption(field, value);
      });
    } else {
      client.clickOption(fields, value);
    }
  });

  if (typeof callback === 'function') {
    callback.call(client);
  }

  return client;
};