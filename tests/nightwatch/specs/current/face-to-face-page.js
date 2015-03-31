'use strict';

var util = require('util');
var common = require('../../modules/common-functions');

module.exports = {
  'Start page': common.startPage,

  'Categories of law (Your problem)': function(client) {
    client
      .assert.urlContains('/problem')
      .assert.containsText('h1', 'What do you need help with?')
      .click('input[name="categories"][value="clinneg"]')
      .assert.attributeEquals('input[name="categories"][value="clinneg"]', 'checked', 'true')
      .submitForm('form')
    ;
  },

  'Face-to-face page': function(client) {
    client
      .waitForElementVisible('.legal-adviser-search', 5000)
      .assert.urlContains('/face-to-face')
      .assert.containsText('h1', 'You may be able to get free advice from a legal adviser')
    ;

    client.end();
  }

};
