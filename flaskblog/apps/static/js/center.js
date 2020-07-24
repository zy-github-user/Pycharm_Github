$(function () {
    $('#InputPhone').blur(function () {
        let phone = $(this).val();
        let span_ele = $(this).next('span');
        if (phone.length == 11) {
            span_ele.text('');
            $.get('user/check_phone', {phone: phone}, function (data) {
                    //console.log(data);
                    if (data.code != 200) {
                        span_ele.css({"color": "#ff0011", "font-size": "12px"});
                        span_ele.text(data.msg);
                    }
                }
            )
        } else {
            span_ele.css({"color": "#ff0011", "font-size": "12px"});
            span_ele.text('手机格式错误');
        }

    })
})();

