var express = require('express');
var router = express.Router();

/* GET augmentation page */
router.get('/', function(req, res, next) {
  res.render('augmentation_result', { title: 'Augmentation_result' });
});

module.exports = router;
