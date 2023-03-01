from flask import Blueprint
from flask import render_template_string

from module_29_testing.hw.flaskr.log import log

bp = Blueprint('errors', __name__)


@bp.app_errorhandler(404)
def handle_404(err):
    log.exception('Incorrect query')
    return render_template_string("<h1>404 Error</h1><h2> Incorrect query </h2>"), 404


@bp.app_errorhandler(405)
def handle_405(err):
    log.exception('Incorrect query')
    return render_template_string("<h1>405 Error</h1><h2> Incorrect query </h2>"), 405


@bp.app_errorhandler(500)
def handle_500(err):
    log.exception('InternalServerError')
    return render_template_string("<h1>500 Error</h1><h2> InternalServerError </h2>"), 500


# @bp.errorhandler(InternalServerError)
# def handle_exception(e: InternalServerError):
#     original: Optional[Exception] = getattr(e, "original_exception", None)
#
#     if isinstance(original, FileNotFoundError):
#         with open("invalid_error.log", "a") as fo:
#             fo.write(
#                     f"Tried to access {original.filename}. Exception info: {original.strerror}\n"
#             )
#     elif isinstance(original, OSError):
#         with open("invalid_error.log", "a") as fo:
#             fo.write(f"Unable to access a card. Exception info: {original.strerror}\n")
#
#     return "Internal server error", 500