window.onload = function () {
    let firefoxAgent = userAgentString.indexOf("Firefox") > -1;

    var options = {"fileExt": false, "disableScroll": true};
    if (firefoxAgent) {
        options["scrollZoomFactor"] = -0.5;
    }

    $(document).ready(function() {
        var gallery = $('#gallery a').simpleLightbox(options);
    });
};
