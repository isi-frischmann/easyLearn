if (typeof self.options !== 'undefined') {
    timer = setTimeout(function () {
        self.checkSelection();
    }, self.options.delay);
}

$(document).ready(function () {
    $('href, #a-nav').on('click', function () {
        ('#part').load()
    })

    $('href, #finish_activity').click(function () {
        console.log("Finish clicked")
            ('#part').load()
    })
});