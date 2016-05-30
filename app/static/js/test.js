function move_on(element,far,to,cishu,time) {
    var add=(to%2==1)?true:false;
    var num=(to<3)?((element.style.marginLeft==="")?0:parseInt(element.style.marginLeft)):((element.style.marginTop==="")?0:parseInt(element.style.marginTop));
    var max=(to%2==1)?(num+far):num;
    var min=(to%2==1)?num:(num+far);
    var time=setInterval(function  () {
        if(add){
            num++;
            (to<3)?(element.style.marginLeft=num+"px"):(element.style.marginTop=num+"px");
            if(num>=max){
                add=false;
                cishu--;
                if(cishu==0){clearInterval(time)}
            }
        }else{
            num--;
            (to<3)?(element.style.marginLeft=num+"px"):(element.style.marginTop=num+"px");
            if(num<=min){
                add=true;
                cishu--;
                if(cishu==0){clearInterval(time)}
            }
        }
    },time);
}
// http://www.saber.xn--6qq986b3xl/js%E5%81%9A%E7%9A%84%E5%85%83%E7%B4%A0%E4%B8%8D%E9%97%B4%E6%96%AD%E6%9D%A5%E5%9B%9E%E7%A7%BB%E5%8A%A8%E7%9A%84%E6%95%88%E6%9E%9C.html#comment-3050