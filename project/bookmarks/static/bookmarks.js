function bookmarkSet($button) {
    $button.addClass('active');
    $(".bookmark-unbookmark", $button).removeClass('hidden');
    $(".bookmark-bookmark", $button).addClass('hidden');
}

function bookmarkUnset($button) {
    $button.removeClass('active');
    $(".bookmark-unbookmark", $button).addClass('hidden');
    $(".bookmark-bookmark", $button).removeClass('hidden');
}

$(document).on('click', '.bookmark-button', function () {
    // Toggle the status of bookmarked/not-bookmarked
    var $button = $(this);
    $.post($button.data('toggle-href'), function (data) {
        if (data.action == 'set')
            bookmarkSet($button);
        else if (data.action == 'unset')
            bookmarkUnset($button);
    }, 'json');
});

$(".bookmark-button.bookmark-needs-loading").each(function () {
    // If we're using the ajax-load version of the widget, it doesn't know the
    // initial state of bookmarked/not-bookmarked. This gets the status and
    // removes all the loading stuff.
    var $button = $(this);
    console.log("needs-loading");
    $.get($button.data('get-href'), function (data) {
        $button.prop('disabled', false);
        $button.removeClass('bookmark-needs-loading');
        $(".bookmark-loading", $button).addClass('hidden');
        if (data.set)
            bookmarkSet($button);
        else
            bookmarkUnset($button);
    }, 'json');
});