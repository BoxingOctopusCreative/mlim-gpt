from flask import Flask, request, jsonify, render_template
from flasgger import Swagger, swag_from
import mlim_gpt

cfg             = mlim_gpt.Config()
app             = Flask(__name__)
listen          = cfg.listen
port            = cfg.port
app.debug       = cfg.debug_mode
app.secret_key  = cfg.app_key
swag            = mlim_gpt.SwaggerDef()
swag_tpl        = swag.template
swag_cfg        = swag.swagger_config
swagger         = Swagger(app, template=swag_tpl, config=swag_cfg)

@app.route('/playlist', methods=['GET'])
@swag_from('swagger/playlist.yaml')
def playlist():
    spotify_client_id     = request.args.get('spotify_client_id')
    spotify_client_secret = request.args.get('spotify_client_secret')
    plist_id              = request.args.get('playlist_id')
    playlist              = mlim_gpt.Playlist(playlist_id=plist_id,
                                              spotify_client_id=spotify_client_id,
                                              spotify_client_secret=spotify_client_secret)

    return jsonify(playlist.get_tracks())

@app.route('/blogpost', methods=['GET'])
@swag_from('swagger/blogpost.yaml')
def blogpost():
    spotify_client_id     = request.args.get('spotify_client_id')
    spotify_client_secret = request.args.get('spotify_client_secret')
    openai_api_key        = request.args.get('openai_api_key')
    prompt                = request.args.get('prompt')
    plist_id              = request.args.get('playlist_id')
    blogpost              = mlim_gpt.BlogPost(spotify_client_id=spotify_client_id,
                                              spotify_client_secret=spotify_client_secret,
                                              playlist_id=plist_id, 
                                              prompt=prompt, 
                                              openai_api_key=openai_api_key)
    
    return jsonify(blogpost.generate_blog_post())

@app.route('/htmlpost', methods=['GET'])
def htmlpost():
    spotify_client_id     = request.args.get('spotify_client_id')
    spotify_client_secret = request.args.get('spotify_client_secret')
    openai_api_key        = request.args.get('openai_api_key')
    prompt                = request.args.get('prompt')
    plist_id              = request.args.get('playlist_id')
    blogpost              = mlim_gpt.BlogPost(spotify_client_id=spotify_client_id,
                                              spotify_client_secret=spotify_client_secret,
                                              playlist_id=plist_id, 
                                              prompt=prompt, 
                                              openai_api_key=openai_api_key)
    post = blogpost.generate_blog_post()

    return render_template('blogpost.html.j2', post=post)

if __name__ == '__main__':
    app.run(host=listen, port=port)
