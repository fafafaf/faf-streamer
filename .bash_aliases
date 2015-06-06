twitch() {
     INRES="1920x1080" # input resolution
     OUTRES="1920x1080" # output resolution
     FPS="30" # target FPS
     GOP="60" # i-frame interval, should be double of FPS, 
     GOPMIN="15" # min i-frame interval, should be equal to fps, 
     THREADS="4" # max 6
     CBR="3000k" # constant bitrate (should be between 1000k - 3000k)
     QUALITY="ultrafast"  # one of the many FFMPEG preset
     AUDIO_RATE="44100"
     STREAM_KEY=$(cat ~/.twitch_key) # use the terminal command Streaming streamkeyhere to stream your video to twitch or justin
     SERVER="live-iad" # twitch server in frankfurt, see http://bashtech.net/twitch/ingest.php for list
     
     avconv -f x11grab -s "$INRES" -r "$FPS" -i :0.0 -f pulse -i default -f flv -ar 44100 -ac 2 -b:a 96k \
       -vcodec libx264 -g $GOP -keyint_min $GOPMIN -b:v $CBR -minrate $CBR -maxrate $CBR -pix_fmt yuv420p -preset $QUALITY \
       -s $OUTRES -acodec aac -threads $THREADS -strict experimental \
       -bufsize $CBR "rtmp://$SERVER.twitch.tv/app/$STREAM_KEY"
}

download_replay() {
    wget --content-disposition http://content.faforever.com/faf/vault/replay_vault/replay.php?id=$1
}

start_replay() {
    export DISPLAY=:0
    export WINEDEBUG=-all 
    if [ -z $1 ]; then
        echo "expects replay id in first param";
    else
        python faf/src/main.py $(pwd)/$1 1>/dev/null 2>&1
    fi
}
