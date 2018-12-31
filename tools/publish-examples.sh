#!/usr/bin/env bash

set -eu
set -o pipefail

examples_dir="published-examples"
gzipped_examples_dir="published-examples-gzip"

gzip_examples()
{
    echo "Gzipping examples files"
    rm -r ${gzipped_examples_dir} || true
    cp -R ${examples_dir} ${gzipped_examples_dir}
    find ${gzipped_examples_dir} -type f ! -name '*.gz' \
        -exec gzip -9 "{}" \; \
        -exec mv "{}.gz" "{}" \;
}

publish_examples()
{
    echo "pushing examples to s3://awe-static-files/examples"
    aws --profile awe-publisher s3 cp \
        ${gzipped_examples_dir} s3://awe-static-files/examples \
        --recursive \
        --acl public-read \
        --content-encoding gzip
}

main()
{
    echo "Publishing examples"
    gzip_examples
    publish_examples
}

main
