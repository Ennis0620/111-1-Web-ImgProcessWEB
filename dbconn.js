const config = require("./dbconfig");
const sql = require("mssql");


const sql_getCustomers = "SELECT * FROM Customers";
const sql_getCustomersId = "SELECT * FROM Customers WHERE CustomerId = @CustomerId";
const sql_storeImgs = "INSERT INTO Image(owner,image_path) VALUES (@owner,@image_path)";
const sql_showImgs = "SELECT owner, image_path FROM Image INNER JOIN User_id ON User_id.ID = Image.owner"; 
const sql_showAugImgs = "SELECT owner, image_augmen FROM Image_aug INNER JOIN User_id ON User_id.ID = Image_aug.owner";
const sql_storeImgsVisual = "INSERT INTO Image_visual(owner,image_visual) VALUES (@owner,@image_visual)";
const sql_showVisualImgs = "SELECT TOP 1 owner,time,image_visual_result FROM Image_visual_result INNER JOIN User_id ON User_id.ID = (@owner) ORDER BY time DESC";

 

//全部query
async function getCustomers(){
    try{
        let pool = await sql.connect(config);
        let Customers = await pool.request().query(sql_getCustomers);
        return Customers.recordsets;
    }
    catch (error){
        console.log(error);
    }
}

//依照id來query
async function getCustomer(customerId){
    try{
        let pool = await sql.connect(config);
        let Customers = await pool.request()
        .input("CustomerId",sql.Int,customerId)
        .query(sql_getCustomersId);
        return Customers.recordsets;
    } 
    catch (error){
        console.log(error);
    }
}

//aug影像上傳 儲存影像資料
async function storeImgs(owner,image_path){
    try{
        let pool = await sql.connect(config);
        let Imgs = await pool.request()
        .input("owner",sql.Int,owner)
        .input("image_path",sql.VarChar,image_path)
        .query(sql_storeImgs);
        //return Imgs.recordsets;
    }
    catch (error){
        console.log(error);
    }
}
//讀取影像資料
async function showImgs(User_id){
    try{
        let pool = await sql.connect(config);
        let Imgs = await pool.request()
        .input("User_id",sql.Int,User_id)
        .query(sql_showImgs);
            return Imgs.recordsets;
    }
    catch (error){
        console.log(error);
    }
}

//讀取aug後的影像資料
async function showAugImgs(User_id){
    try{
        let pool = await sql.connect(config);
        let Imgs = await pool.request()
        .input("User_id",sql.Int,User_id)
        .query(sql_showAugImgs);
            return Imgs.recordsets;
    }
    catch (error){
        console.log(error);
    }
}

//visual影像上傳
async function storeImgsVisual(owner,image_visual){
    try{
        let pool = await sql.connect(config);
        let Imgs = await pool.request()
        .input("owner",sql.Int,owner)
        .input("image_visual",sql.VarChar,image_visual)
        .query(sql_storeImgsVisual);
        //return Imgs.recordsets;
    }
    catch (error){
        console.log(error);
    }
}

//讀取visual_result資料表的最後一筆資料
async function showVisualImgs(owner){
    try{
        let pool = await sql.connect(config);
        let Imgs = await pool.request()
        .input("owner",sql.Int,parseInt(owner))
        .query(sql_showVisualImgs);
            return Imgs.recordsets;
    }
    catch (error){
        console.log(error);
    }
}

module.exports = {
    getCustomers: getCustomers,
    getCustomer: getCustomer,
    storeImgs : storeImgs,
    showImgs : showImgs,
    showAugImgs : showAugImgs,
    storeImgsVisual : storeImgsVisual,
    showVisualImgs : showVisualImgs,
}