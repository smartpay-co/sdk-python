#!/bin/bash

FILES=smartpay/schemas/*.json

for f in $FILES; do
  echo $f
  OUT=smartpay/schemas/$(basename -s .jtd.json $f | sed -e 's/[.-]/_/g').py
  printf '%s\n\n%s%s\n' "import jtd" "$(basename -s .jtd.json $f | sed -e 's/[.-]/_/g')_schema = jtd.Schema.from_dict(" "$(cat $f | sed -e 's/ true/ True/' | sed -e 's/ false/ False/')" ")" > $OUT
  autopep8 --in-place $OUT
done

echo "done"