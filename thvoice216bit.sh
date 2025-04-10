# cd ./data/porameht_voice_th169k/wavs/

# mkdir -p fixed_wavs

# for f in *.wav; do
#     ffmpeg -y -loglevel error -i "$f" -ar 22050 -ac 1 -c:a pcm_s16le "fixed_wavs/$f"
# done

cd ./data/porameht_voice_th169k/wavs

for i in $(seq -w 142642 169550); do
  rm -f "audio_${i}.wav"
done

# rm -f "audio_*.wav"