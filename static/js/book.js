var viewer;

function show_viewer(image) {
    viewer = ImageViewer();
    viewer.show(image.src);
}

window.onload = function () {
    document.querySelectorAll(".book-image").forEach(function (elem) {
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

function show_gallery_viewer(low_res_path, hi_res_path) {
    viewer = ImageViewer();
    viewer.show(low_res_path, hi_res_path);
}
