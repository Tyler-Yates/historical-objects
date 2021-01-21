var viewer;

function show_viewer(image) {
    viewer = ImageViewer();
    var period_index = image.src.lastIndexOf(".");
    viewer.show(image.src, image.src.substring(0, period_index) + "-hi" + image.src.substring(period_index));
}

window.onload = function () {
    document.querySelectorAll(".plate-image").forEach(function (elem) {
        elem.onclick = function () {
            show_viewer(elem);
        };
    });

    var hide_on_escape = function (e) {
        if (e.key === 'Escape') {
            viewer.hide();
        }
    };
    document.addEventListener('keydown', hide_on_escape, false);
};
