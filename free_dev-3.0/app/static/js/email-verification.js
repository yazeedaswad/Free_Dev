function validate(){
    var mail = doccument.getElementById("email").value;
    var regx = /^([a-zA-Z0-9\._]+)@([a-zA-Z0-9])+.([a-z]+)(.[a-z]+)?$/;

    if(regx.test(mail)){
        console.log("Valid Email");
        return true;   
    }
    else{
        console.log("invalid Email");
        return false;
    }
}