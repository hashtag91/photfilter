const pic_div = document.querySelector('.pic-div')
let image = document.querySelector('.image')
let pic_div_width = pic_div.offsetWidth
let pic_div_height = pic_div.offsetHeight
image.style.height = '100%'
image.style.width = pic_div_width - pic_div_height
function apply_filter(img_filter){
    const img_element = document.querySelector('.image');
    $.ajax({
        url:'/apply_filter',
        type:'post',
        data: {'filter':img_filter},
        success: function(response){
            img_element.src = response['path']
        },
        error: function(){
            alert('Une erreur s\'est produite')
        }
    })
}
const buttons = document.querySelectorAll('#filter-btn')
let bg_img = ['static/temp/original.jpg','static/temp/gray.jpg','static/temp/threshold.jpg','static/temp/canny.jpg','static/temp/blur.jpg'];
for (let i=0; i<bg_img.length; i++){
    buttons[i].style.backgroundImage = 'url(\''+bg_img[i] +'\')'
    console.log('url(\''+bg_img[i] +'\')')
}