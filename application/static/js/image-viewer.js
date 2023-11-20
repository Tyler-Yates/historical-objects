window.onload = function () {
    let userAgentString = navigator.userAgent;
    let firefoxAgent = userAgentString.indexOf("Firefox") > -1;

    var options = {"fileExt": false, "disableScroll": true, "animationSpeed": 0, "fadeSpeed": 0};
    if (firefoxAgent) {
        options["scrollZoomFactor"] = -0.5;
        options["overlayOpacity"] = 1.0;
    }

    $(document).ready(function() {
        var gallery = $('.image-gallery a').simpleLightbox(options);
    });
};
