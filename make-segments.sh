ffmpeg -i LwekZs3Sp8g.webm -c:v libx264 -crf 23 -vf scale=320:240 -c:a aac -b:a 64k -strict experimental -hls_time 15 -hls_playlist_type vod -hls_segment_filename "segments/segment_%03d.ts" ./segments/output.m3u8
