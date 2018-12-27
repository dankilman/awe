#!/usr/bin/env bash

set -eu
set -o pipefail

version="$(python setup.py --version)"
dist_file="dist/awe-${version}-py2-none-any.whl"
master_branch="master"
current_branch="$(git symbolic-ref --short HEAD)"
origin_master="origin/master"
build_status_url="https://circleci.com/api/v1.1/project/github/dankilman/awe/tree/${master_branch}?limit=1"

exit_with()
{
    echo "$@"
    exit 1
}

validate()
{
    echo "Running validations"
    test "${current_branch}" = "${master_branch}" || exit_with "Current branch is not ${master_branch}"
    git diff --quiet "${current_branch}" "${origin_master}" || exit_with "local version differs from origin"
    test -f "${dist_file}" || exit_with "no dist found"
    local full_status="$(curl ${build_status_url} 2> /dev/null)"
    local status="$(echo ${full_status} | jq '.[].status' -r)"
    local status_commit="$(echo ${full_status} | jq '.[].vcs_revision' -r)"
    local local_commit="$(git rev-parse HEAD)"
    test "${status}" = 'success' || exit_with "Last ${master_branch} build failed"
    test "${status_commit}" = "${local_commit}" || exit_with "CircleCI commit sha differs from local commit sha"
}

tag()
{
    echo "Tagging and pushing tag"
    git tag "${version}"
    git push origin "${version}"
}

publish_pypi()
{
    echo "Uploading to pypi"
    twine upload "${dist_file}"
}

publish_static_files()
{
    echo "pushing static files to s3://awe-static-files"
    aws --profile awe-publisher s3 cp \
        awe/resources/client/awe/build s3://awe-static-files/dist/${version} \
        --recursive \
        --acl public-read \
        --exclude "*.map"
}

main()
{
    echo "Publishing version ${version}"
    validate
    tag
    publish_pypi
    publish_static_files
}

main
