//DataBase
var db = require('./dbconn');

var express = require('express');
var bodyParser = require('body-parser');
var cors = require('cors');
var app = express();
var router = express.Router();

//WEB
const hbs = require('hbs');
const path = require('path');
const cookieParser = require('cookie-parser');
const logger = require('morgan');
const multer = require('multer');
const sharp = require("sharp");
const fs = require("fs");
const AdmZip = require("adm-zip");

//python
const { PythonShell } = require('python-shell');

//添加前端Router
var indexRouter = require('./routes/index');
var augmentationRouter = require('./routes/augmentation');
var augmentation_chooseRouter = require('./routes/augmentation_choose');
var augmentation_resultRouter = require('./routes/augmentation_result');
var ImagelabelingRouter = require('./routes/Imagelabeling');
var ImageprocessingRouter = require('./routes/Imageprocessing');
var VisualizationRouter = require('./routes/Visualization');
var Visualization_chooseRouter = require('./routes/Visualization_choose');
var Visualization_resultRouter = require('./routes/Visualization_result');
var usersRouter = require('./routes/users');
const { response } = require('express');

//__dirname + '/views/partials'
hbs.registerPartials(path.join(__dirname, '/views/partials'), (err) => { });

// view engine setup hbs 
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'hbs');
//ejs
//app.set('view engine', 'ejs');

//WEB
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.static(path.join(__dirname, '/upload')));
app.use(express.static(path.join(__dirname, '/upload_aug')));
app.use(express.static(path.join(__dirname, '/visual')));
app.use(express.static(path.join(__dirname, '/visual_result')));
//app.use(express.static(path.join(__dirname, '/static/upload')));

//串前端 
app.use('/', indexRouter);
app.use('/augmentation', augmentationRouter);
app.use('/augmentation_choose', augmentation_chooseRouter);
app.use('/augmentation_result', augmentation_resultRouter);
app.use('/Imagelabeling', ImagelabelingRouter);
app.use('/Imageprocessing', ImageprocessingRouter);
app.use('/Visualization', VisualizationRouter);
app.use('/Visualization_choose', Visualization_chooseRouter);
app.use('/Visualization_result', Visualization_resultRouter);
app.use('/users', usersRouter);

//串資料庫 添加Router 
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(cors());
app.use('/api', router);

router.use((req, res, next) => {
    console.log('API');
    next();
})

/*************************************************Augmentation********************************************************/

//augmentation影像上傳
var storage = multer.diskStorage({
    //目標儲存路徑
    destination: function (req, file, cb) {
        //cb(null, __dirname+'/static/upload/')
        cb(null, __dirname + '/upload/')
    },
    //
    filename: function (req, file, cb) {
        const time_stamp = Date.now();
        const dateObj = new Date(time_stamp);
        const year = dateObj.getFullYear();
        const month = dateObj.getMonth() + 1;
        const day = dateObj.getDate();
        const hour = dateObj.getHours();
        const min = dateObj.getMinutes();
        const sec = dateObj.getSeconds();

        const completeTime = year + '_' + month + '_' + day + '_' + hour + '_' + min + '_' + sec;
        cb(null, completeTime + '_' + file.originalname)
    }
})

var upload = multer({ storage: storage })

//profile-upload-multiple
app.post('/profile-upload-multiple', upload.array('profile-files', 10000), function (req, res, next) {

    for (var i = 0; i < req.files.length; i++) {
        //console.log(req.files[i]);
        //user_name
        const user_id = 1;
        //儲存的影像名稱
        const img_name = req.files[i].filename;
        console.log(req.files[i]);
        //儲存的img
        //var img = fs.readFileSync(`http://localhost:3000/${img_name}`);
        //const img = `http://localhost:3000/${img_name}`;
        //儲存日期
        //time =  img_name.split('_');
        //const real_time = time[0]+'-'+time[1]+'-'+time[2]+' '+time[3]+':'+time[4]+':'+time[5];
        //console.log(real_time);
        //上傳影像
        db.storeImgs(user_id, img_name).then(dataset => {
            console.log(`STORE Image:${img_name}`);
        });
    }
    //response += "<h3 >Files uploaded successfully.</h3><br>"
    //res.sendFile(__dirname + '/profile-upload-multiple')
    res.redirect('/augmentation_choose')
    //res.send(response)//res.redirect('/augmentation_choose')
})

//augmentation取得該使用者所上傳的影像
app.get('/augmentation_choose/:user_id', function(req, res) {
    console.log('req:'+ req);
    db.showImgs(req.params.user_id).then(dataset => {
        //console.log(`SHOW Image:${JSON.stringify(dataset)}`);
        return res.json(dataset);
    });
}); 

//取得選擇的augmentation方式
app.get('/call/aug', augPython)

//顯示使用者augmentation後的結果
app.get('/Augmentation_result/:user_id', function(req, res) {
    console.log('req:'+ req);
    db.showAugImgs(req.params.user_id).then(dataset => {
        //console.log(`SHOW Image:${JSON.stringify(dataset)}`);
        return res.json(dataset);
    });
}); 

//Zip Aug檔案的圖片
app.get('/zip/:user_id', function(req, res){
    const zip = new AdmZip();

    let imgPath = [];
    db.showAugImgs(req.params.user_id).then(dataset => {
        jsonDataset = JSON.stringify(dataset);
        console.log(`AugImgs:${JSON.stringify(dataset[0])}`);
        console.log(`img_name:${dataset[0]}`);

        for(key in dataset[0]) {
            console.log(`key:${dataset[0][key]["image_augmen"]}`);
            const imagePath = dataset[0][key]["image_augmen"];
            imgPath.push(imagePath);
            zip.addLocalFile(__dirname+"/upload_aug/"+ imagePath);
        }
        
        
        let outputPath = Date.now() + "output.zip";
        fs.writeFileSync(outputPath,zip.toBuffer());
        //下載zip檔案
        res.download(outputPath,(err)=>{
            if(err){
                
                imgPath.forEach(file=>{
                    //fs.unlinkSync(__dirname+"/upload_aug/"+ file);
                    res.send("Error in downloadinf zip");
                }); 

            }
            //下載完就移除augmentation資料夾內的圖片
            /*
            imgPath.forEach(file=>{
                fs.unlinkSync(__dirname+"/upload_aug/"+ file);
            });
            fs.unlinkSync(outputPath)
            */
        });

        //return res.json(dataset);
    });
});

//augPython
function augPython(req, res) {

    let options = {
        args:
            [
                req.query.user_id,
                req.query.vertical_flip,
                req.query.horizontal_flip,
                req.query.histogramEqualColor,
                req.query.adjust_gamma,
                req.query.rotation,
                //req.query.erode,
                //req.query.dilate,
                //req.query.opening,
                //req.query.closing,
                //req.query.Gradient,
            ]
    }
    PythonShell.run('augmentation.py', options, (err, data) => {
        if (err) res.send(err)
        //const parsedString = JSON.parse(data)
        /*
        console.log(`user_id: ${parsedString.User_id}, 
                    vertical_flip: ${parsedString.Vertical_flip},
                    horizontal_flip: ${parsedString.Horizontal_flip},
                    histogramEqualColor: ${parsedString.HistogramEqualColor},
                    adjust_gamma: ${parsedString.Adjust_gamma},`
                     )

        res.json(parsedString)
        */
    })
    res.redirect('/augmentation_result')
}


/*************************************************Visualization********************************************************/
//Visualization影像上傳
var storage_Visualization = multer.diskStorage({
    //目標儲存路徑
    destination: function (req, file, cb) {
        cb(null, __dirname + '/visual/')
    },
    //
    filename: function (req, file, cb) {
        const time_stamp = Date.now();
        const dateObj = new Date(time_stamp);
        const year = dateObj.getFullYear();
        const month = dateObj.getMonth() + 1;
        const day = dateObj.getDate();
        const hour = dateObj.getHours();
        const min = dateObj.getMinutes();
        const sec = dateObj.getSeconds();

        const completeTime = year + '_' + month + '_' + day + '_' + hour + '_' + min + '_' + sec;
        cb(null, completeTime + '_' + file.originalname)
    }
})

var visual = multer({ storage: storage_Visualization })

//profile-upload-multiple-Visual
app.post('/profile-upload-multiple-Visual', visual.array('profile-files', 10000), function (req, res, next) {

    for (var i = 0; i < req.files.length; i++) {
        //console.log(req.files[i]);
        //user_name
        const user_id = 1;
        //儲存的影像名稱
        const img_name = req.files[i].filename;
        //console.log(req.files[i])
        //上傳影像
        /*
        db.storeImgsVisual(user_id, img_name).then(dataset => {
            console.log(`STORE Image Visual:${img_name}`);
        });
        */
    }
    res.redirect('/Visualization_choose')
})


//取得選擇的visualization方式
app.get('/call/visual', visualPython)

function visualPython(req, res) {

    //console.log(req.query);
    let options = {
        args:
            [
                req.query.user_id,
                req.query.method,
                req.query.draw_method,
                req.query.k_means,
            ]
    }
    
    PythonShell.run('Visualization.py', options, (err, data) => {
        if (err) res.send(err)
        
        const parsedString = JSON.parse(data);
        //console.log(`user_id: ${parsedString.User_id},
        //            save_name: ${parsedString.save_name}`);
        let User_id = `${parsedString.User_id}`;
        let save_name = `${parsedString.save_name}`;
        //res.json(parsedString)
        
    })
    res.redirect('/Visualization_result')
}

//顯示使用者visualization後的結果
app.get('/Visualization_result/:id', function(req, res) {
    console.log('req:'+ req);
    db.showVisualImgs(req.params.id).then(dataset => {
        console.log(`Visual Image name:${JSON.stringify(dataset[0])}`);
        return res.json(dataset);
    });
}); 


//ImageProcess


const port = process.env.port || 3000;
app.listen(port);
console.log(`API Listening... at port: ${port}`);

module.exports = app;



