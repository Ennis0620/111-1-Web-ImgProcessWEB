/*
const images_input = document.querySelector('#uploadImgs');
var uploaded_images = "";
if (images_input) {
    images_input.addEventListener("change", function () {

        const reader = new FileReader(); 
        reader.addEventListener("load",()=>{
            uploaded_images = reader.result;
            document.querySelector('#display_imgs').style.backgroundImage = `url(${uploaded_images})`;
        });
        reader.readAsDataURL(this.files[0]);
    })
}
*/
let fileInput = document.getElementById("profile-files");
let imageContainer = document.getElementById("images");
let numOfFiles = document.getElementById("num-off-files");

function previewFile() {
    imageContainer.innerHTML= "";
    //numOfFiles.textContent = `${fileInput.files.length} Files Select`;
    for (i of fileInput.files){
        let reader = new FileReader();
        let figure = document.createElement("figure");
        let figCap = document.createElement("figcaption");
        figCap.innerHTML = i.name;
        figure.appendChild(figCap);
        reader.onload=()=>{
            let img = document.createElement("img");
            img.setAttribute("src",reader.result);
            figure.insertBefore(img,figCap);
        }
        imageContainer.appendChild(figure);
        reader.readAsDataURL(i);
    }

    /*
    const preview = document.querySelector('img');
    const file = document.querySelector('input[type=file]').files[0];
    const reader = new FileReader();
  
    reader.addEventListener("load", function () {
      // convert image file to base64 string
      preview.src = reader.result;
    }, false);
  
    if (file) {
      reader.readAsDataURL(file);
    }
    */
  }