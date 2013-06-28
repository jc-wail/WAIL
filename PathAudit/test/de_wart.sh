#!/s/std/bin/bash
FILES=./*.warts
for f in $FILES
do
  echo "Processing $f file..."
  # take action on each file. $f store current file name
  /scratch/jpchaba/scamper/scamper-cvs-20110803/utils/sc_analysis_dump/sc_analysis_dump -C "$f" > "$f.txt"
done