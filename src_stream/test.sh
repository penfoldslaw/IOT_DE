config_file="../src_stream/config.cfg"

topic_1=$(awk -F ' = ' '/topic_1/ {print $2}' "$config_file")
topic_2=$(awk -F ' = ' '/topic_2/ {print $2}' "$config_file")


echo "$topic_1"
echo "$topic_2"