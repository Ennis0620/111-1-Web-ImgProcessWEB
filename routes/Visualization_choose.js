var express = require('express');
var router = express.Router();

/* GET augmentation page */
router.get('/', function(req, res, next) {
  res.render('Visualization_choose', { title: 'Visualization_choose' });
});

module.exports = router;
