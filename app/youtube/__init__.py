from flask import Blueprint, request, jsonify

from app.youtube.player import create_youtube_url


youtube_bp = Blueprint(
    "youtube",
    __name__
)


@youtube_bp.route(
    "/play",
    methods=["POST"]
)
def play():

    data = request.get_json(
        silent=True
    ) or {}

    command = data.get(
        "command",
        ""
    ).strip()

    if not command:

        return jsonify({
            "success": False,
            "message": "Song name is required"
        }), 400

    url = create_youtube_url(
        command
    )

    if not url:

        return jsonify({
            "success": False,
            "message": "Could not find the song"
        }), 404

    return jsonify({
        "success": True,
        "type": "youtube",
        "query": command,
        "url": url
    })
