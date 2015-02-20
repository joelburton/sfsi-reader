$(document).on('click', '.bookmark-button', function () {
    var $button = $(this);
    $.post($button.data('href'), function (data) {
        if (data.action == 'set') {
            $button.addClass('active');
            $(".bookmark-unbookmark", $button).removeClass('hidden');
            $(".bookmark-bookmark", $button).addClass('hidden');
        }
        else if (data.action == 'unset') {
            $button.removeClass('active');
            $(".bookmark-unbookmark", $button).addClass('hidden');
            $(".bookmark-bookmark", $button).removeClass('hidden');
        }
    }, 'json');
});