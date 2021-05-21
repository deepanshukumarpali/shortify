function validateCustomCode() {
          
    var TCode = document.getElementById("customCode").value,msg = "ok";
    for (var i = 0; i < TCode.length; i++) {
            var char1 = TCode.charAt(i);
            var cc = char1.charCodeAt(0);

            if ((cc > 47 && cc < 58) || (cc > 64 && cc < 91) || (cc > 96 && cc < 123) || char1 == '-') {
            } else {
                msg = "Remove " + char1 + " from custom url name";
                break;
            }
        }

    var string = document.getElementById("longUrl").value;
    if(! isValidURL(string)) { msg = "Invalid URL";}

    if(msg == "ok") return true;
    alert(msg);
    return false;

}

function isValidURL(str) {
    var regex = /(http|https):\/\/(\w+:{0,1}\w*)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%!\-\/]))?/;
    if(!regex .test(str)) { return false;
    } else { return true;
    }

    };