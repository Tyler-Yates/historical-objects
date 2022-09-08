from flask import Blueprint, current_app, render_template

MAIN_BLUEPRINT = Blueprint("routes", __name__)


@MAIN_BLUEPRINT.route("/debug")
def debug_page():
    problematic_medals = {}
    for medal in current_app.config["data"]["medals"].values():
        if medal.sort_year == -1:
            problematic_medals[medal.id] = "No sort_year"

    problematic_books = {}
    for book in current_app.config["data"]["books"].values():
        if book.sort_year == -1:
            problematic_books[book.id] = "No sort_year"

    problematic_plates = {}
    for plate in current_app.config["data"]["plates"].values():
        if plate.sort_year == -1:
            problematic_plates[plate.id] = "No sort_year"

    return render_template(
        "debug.html",
        medals=current_app.config["data"]["medals"],
        problematic_medals=problematic_medals,
        books=current_app.config["data"]["books"],
        problematic_books=problematic_books,
        plates=current_app.config["data"]["plates"],
        problematic_plates=problematic_plates,
    )


@MAIN_BLUEPRINT.route("/")
def home_page():
    return render_template("index.html")


@MAIN_BLUEPRINT.route("/medals")
def medals_page():
    return render_template("medals.html", medals=current_app.config["data"]["medals"].values())


@MAIN_BLUEPRINT.route("/medals/<medal_id>")
def medal_page(medal_id):
    return render_template("medal.html", medal=current_app.config["data"]["medals"][medal_id])


@MAIN_BLUEPRINT.route("/books")
def books_page():
    return render_template("books.html", books=current_app.config["data"]["books"].values())


@MAIN_BLUEPRINT.route("/books/<book_id>")
def book_page(book_id):
    book = current_app.config["data"]["books"][book_id]
    return render_template("book.html", book=book, gallery=book.gallery_images)


@MAIN_BLUEPRINT.route("/plates")
def plates_page():
    return render_template("plates.html", plates=current_app.config["data"]["plates"].values())


@MAIN_BLUEPRINT.route("/plates/<plate_id>")
def plate_page(plate_id):
    return render_template("plate.html", plate=current_app.config["data"]["plates"][plate_id])


@MAIN_BLUEPRINT.route("/references")
def references_page():
    return render_template("references.html")


@MAIN_BLUEPRINT.route("/about")
def about_page():
    return render_template("about.html")
