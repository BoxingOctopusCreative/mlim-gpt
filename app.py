from flask import Flask, request, jsonify, Response
from flasgger import Swagger, swag_from
import mlim_gpt

cfg             = mlim_gpt.Config()
app             = Flask(__name__)
app.debug       = cfg.debug_mode
app.secret_key  = cfg.app_key
swag            = mlim_gpt.SwaggerDef()
swag_tpl        = swag.template
swag_cfg        = swag.swagger_config
swagger         = Swagger(app, template=swag_tpl, config=swag_cfg)

@app.route('/playlist', methods=['GET'])
@swag_from('swagger/playlist.yaml')
def playlist():
    playlist_id = request.args.get('playlist_id')
    playlist    = mlim_gpt.Playlist(playlist_id)

    return jsonify(playlist.get_tracks())

@app.route('/blogpost', methods=['GET'])
@swag_from('swagger/blogpost.yaml')
def blogpost():
    playlist_id = request.args.get('playlist_id')
    playlist    = mlim_gpt.Playlist(playlist_id)
    blogpost    = mlim_gpt.BlogPost(playlist)
    
    return jsonify(blogpost.generate_blogpost())

if __name__ == '__main__':
    app.run(host=cfg.listen, port=cfg.port)
