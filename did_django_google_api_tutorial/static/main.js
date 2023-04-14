// function DirectionsToggle(){
//   var el = $('#dir-toggle');
//   var dir_table = $('#dir-table')
//   if (dir_table.attr("hidden") == "hidden") {
//     dir_table.fadeIn()
//     dir_table.removeAttr("hidden")
//     el.html('hide <a href="javascript:void(0)" onclick="DirectionsToggle()">here')
//   } else {
//     dir_table.fadeOut()
//     dir_table.attr("hidden", "hidden")
//     el.html('click <a href="javascript:void(0)" onclick="DirectionsToggle()">here')
//   }
// }


// function ShowAlert(title, message, type, redirect){
//
//     if (redirect){
//       toastr[type](message, title, {
//           positionClass: 'toast-bottom-right',
//           closeButton: true,
//           progressBar: true,
//           newestOnTop: true,
//           rtl: $("body").attr("dir") === "rtl" || $("html").attr("dir") === "rtl",
//           timeOut: 7500,
//           onHidden: function () {
//             window.location.assign(redirect);
//           }
//       });
//     }
//     else{
//       toastr[type](message, title, {
//           positionClass: 'toast-bottom-right',
//           closeButton: true,
//           progressBar: true,
//           newestOnTop: true,
//           rtl: $("body").attr("dir") === "rtl" || $("html").attr("dir") === "rtl",
//           timeOut: 7500,
//
//       });
//
//     }
//
// };
let temp_button_text;

function CustomFormSubmitPost(e) {
    let el = $(e);
    temp_button_text = el.text()
    el.attr('disabled', 'disabled').text("")
        .append('<class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>Loading...');
};

function CustomFormSubmitResponse(e) {
    let el = $(e);
    el.removeAttr('disabled').text(temp_button_text);
};

function showToast(res, msg, redirect) {
    let toastBox = document.getElementById('toastBox');
    let toast = document.createElement('div');
    toast.classList.add('toast');
    toastBox.appendChild(toast);

    if (res.toLowerCase().includes('error')) {
        toast.classList.add('error');
        toast.innerHTML = `<div><i class="fa-solid fa-circle-xmark"></i></div>`;
        toast.innerHTML += `<div>${res}<br>${msg}</div>`;
    }
    if (res.toLowerCase().includes('success')) {
        toast.innerHTML = `<div><i class="fa-solid fa-circle-check"></i></div>`;
        toast.innerHTML += `<div>${res}<br>${msg}</div>`;
    }


    setTimeout(() => {
        toast.remove();
        if (redirect) {
            window.location.assign(redirect);
        }
    }, 3000)

}

function success_ajax(json) {
    let redirect = json['result'] === 'Success' ? '/' : false
    showToast(json["result"], json["message"], redirect);

}

function error_ajax(xhr) {
    showToast("Error", `${xhr.status}:${xhr.responseText}`, false);
}

function showPword() {
    var x = document.getElementsByClassName("password");
    for (let i = 0; i < x.length; i++) {
        if (x[i].type === "password") {
            x[i].type = "text";
        } else {
            x[i].type = "password";
        }
    }
}


"use strict";

function usersignup() {

    let form = $('#signupform')
    form.submit(function (event) {
        event.preventDefault();
        CustomFormSubmitPost($('#signupform button[type=submit]'));

        grecaptcha.ready(function () {
            grecaptcha.execute(recaptcha_site_key, {action: "submit"})
                .then(function (token) {
                    document.getElementById('id_token').value = token;
                    let formdata = form.serialize()
                    $.ajax({
                        url: form.attr("action"),
                        method: form.attr("method"),
                        data: formdata,
                        success: function (json) {
                            success_ajax(json);
                            if (json['result'] === 'Error') {
                                CustomFormSubmitResponse($('#signupform button[type=submit]'));
                            }
                        },
                        error: function (xhr) {
                            error_ajax(xhr);
                            CustomFormSubmitResponse($('#signupform button[type=submit]'));

                        }
                    })
                })
        })

    })
};

function usersignin() {
    let form = $('#signinform')
    form.submit(function (event) {
        event.preventDefault();
        CustomFormSubmitPost($('#signinform button[type=submit]'));

        let formdata = form.serialize()
        $.ajax({
            url: form.attr("action"),
            method: form.attr("method"),
            data: formdata,
            success: function (json) {
                success_ajax(json);
                if (json['result'] === 'Error') {
                    CustomFormSubmitResponse($('#signinform button[type=submit]'));
                }
            },
            error: function (xhr) {
                error_ajax(xhr);
                CustomFormSubmitResponse($('#signinform button[type=submit]'));
            }
        })
    });
};

function userprofile() {

    let form = $('#profileform')
    form.submit(function (event) {
        event.preventDefault();
        CustomFormSubmitPost($('#profileform button[type=submit]'));

        let formdata = form.serialize()
        $.ajax({
            url: form.attr("action"),
            method: form.attr("method"),
            data: formdata,
            success: function (json) {
                success_ajax(json);
                if (json['result'] === 'Error') {
                    CustomFormSubmitResponse($('#profileform button[type=submit]'));
                }
            },
            error: function (xhr) {
                error_ajax(xhr);
                CustomFormSubmitResponse($('#profileform button[type=submit]'));
            }
        })

    })
};

jQuery(document).ready(function () {
    usersignup();
    usersignin();
    userprofile();

});

