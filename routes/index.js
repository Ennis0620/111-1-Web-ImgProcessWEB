var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  //title: 給index.hbs使用
  res.render('index', { title: 'Data Precoessing Web' });
});

module.exports = router;
