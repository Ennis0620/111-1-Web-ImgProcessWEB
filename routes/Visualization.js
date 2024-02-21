var express = require('express');
var router = express.Router();

/* GET augmentation page */
router.get('/', function(req, res, next) {
  res.render('Visualization', { title: 'Auto Visualization' });
});

module.exports = router;
