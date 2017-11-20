//Change Header Color Function

window.addEventListener("scroll",function (){

    if(window.pageYOffset + 100 > document.getElementById('Info').offsetTop){
        document.getElementById('logo').style.color = '#4682B4';
    }else{
        document.getElementById('logo').style.color = '#ffffff';
    }
});