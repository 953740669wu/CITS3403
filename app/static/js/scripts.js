$(document).ready(function() {
    // 处理表单提交
    $('form').on('submit', function(event) {
        event.preventDefault();  // 阻止表单的默认提交行为

        const form = $(this);  // 获取当前表单
        const actionUrl = form.attr('action');  // 获取表单的 action 属性，即提交的 URL
        const formData = form.serialize();  // 序列化表单数据为查询字符串

        // 发送 AJAX POST 请求
        $.post(actionUrl, formData)
        .done(function(data) {
            // 处理请求成功的响应
            if (data.redirect) {
                // 如果响应中包含重定向，保存消息并重定向
                sessionStorage.setItem('message', data.message);
                window.location.href = data.redirect;
            }
        })
        .fail(function(jqXHR) {
            // 处理请求失败的响应
            // 从服务器返回的 JSON 中获取错误消息，并显示
            const message = jqXHR.responseJSON.message;
            $('#flash-content').text(message);
            $('#flash-message').show();
        });
    });

    // 页面加载时检查是否有消息需要显示
    let message = sessionStorage.getItem('message');
    if (message) {
        $('#flash-content').text(message);
        $('#flash-message').show();
        sessionStorage.removeItem('message');  // 显示消息后从 sessionStorage 中移除
    }

    // 处理消息弹窗的关闭
    $('#close-popup').on('click', function() {
        $('#flash-message').hide();  // 隐藏消息弹窗
    });
});