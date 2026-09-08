from Flask import Blueprint, request, jsonify

youtube_bp = Blueprint(
  "youtube",
  __name__
)

@youtube_bp.route(
  "/play" ,
  methods =["POST"]

  )
  def play ():

   data = request.get_json(
    silent = True
    ) or {}
    command = data.get(
    "command" ,
    ""
    ).strip()
    if not command :

  return jsonify({
    "success":"False",
    "message":"there's no song name , mentioned"
  })400
