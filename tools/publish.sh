#!/usr/bin/env bash

set -eu
set -o pipefail

version="$(python setup.py --version)"
dist_file="dist/awe-${version}-py2-none-any.whl"
master_branch="master"
current_branch="$(git symbolic-ref --short HEAD)"
origin_master="origin/master"

exit_with()
{
    echo "$@"
    exit 1
}

validate()
{
    test "${current_branch}" = "${master_branch}" || exit_with "Current branch is not ${master_branch}"
    git diff --quiet "${current_branch}" "${origin_master}" || exit_with "local version differs from origin"
    test -f "${dist_file}" || exit_with "no dist found"
}

tag()
{
    git tag "${version}"
    git push origin "${version}"
}

publish_pypi()
{
    twine upload "${dist_file}"
}

publish_static_files()
{
    aws --profile awe-publisher s3 cp \
        awe/resources/client/awe/build s3://awe-static-files/dist/${version} \
        --recursive \
        --acl public-read \
        --exclude "*.map"
}

main()
{
    validate
    tag
    publish_pypi
    publish_static_files
}

main
