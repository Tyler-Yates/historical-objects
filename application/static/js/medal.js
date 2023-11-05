var viewer;

function show_viewer(image) {
    viewer = ImageViewer();
    console.info(viewer);
    var last_index = image.src.lastIndexOf('/');
    var second_to_last_index = image.src.lastIndexOf('/', last_index - 1);
    var part = image.src.slice(0, second_to_last_index);
    var hiResImageSrc = part + "/hi" + image.src.slice(last_index);
    viewer.show(image.src, hiResImageSrc);
}

window.onload = function () {
    document.querySelectorAll(".medal-image").forEach(function (elem) {
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
