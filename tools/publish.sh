#!/usr/bin/env bash

set -eu
set -o pipefail

version="$(python setup.py --version)"
dist_file="dist/awe-${version}-py2.py3-none-any.whl"
master_branch="master"
current_branch="$(git symbolic-ref --short HEAD)"
origin_master="origin/master"
build_status_url1="https://circleci.com/api/v1.1/project/github/dankilman/awe/tree/${master_branch}?limit=1"
build_status_url2="${build_status_url1}&offset=1"
static_files_dir="awe/resources/client/awe/build"
gzipped_static_files_dir="awe/resources/client/awe/build-gzip"

build_found=''
build37_found=''

exit_with()
{
    echo "$@"
    exit 1
}

validate_ci()
{
    local local_commit="$(git rev-parse HEAD)"
    local build_status_url="$1"
    local full_status="$(curl ${build_status_url} 2> /dev/null)"
    local status="$(echo ${full_status} | jq '.[].status' -r)"
    local status_commit="$(echo ${full_status} | jq '.[].vcs_revision' -r)"
    local job_name="$(echo ${full_status} | jq '.[].workflows.job_name' -r)"
    test "${status}" = 'success' || exit_with "Last ${master_branch} build failed"
    test "${job_name}" = 'build' || test "${job_name}" = "build37" || exit_with "Missing build/build37"
    test "${status_commit}" = "${local_commit}" || exit_with "CircleCI commit sha differs from local commit sha"
    export ${job_name}_found=true
}

validate()
{
    echo "Running validations"
    test "${current_branch}" = "${master_branch}" || exit_with "Current branch is not ${master_branch}"
    git diff --quiet "${current_branch}" "${origin_master}" || exit_with "local version differs from origin"
    test -f "${dist_file}" || exit_with "no dist found"
    validate_ci ${build_status_url1}
    validate_ci ${build_status_url2}
    test "${build_found}" = 'true' || exit_with "Missing build job"
    test "${build37_found}" = 'true' || exit_with "Missing build37 job"
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

gzip_static_files()
{
    echo "Gzipping static files"
    rm -r ${gzipped_static_files_dir} || true
    cp -R ${static_files_dir} ${gzipped_static_files_dir}
    find ${gzipped_static_files_dir} -type f ! -name '*.gz' \
        -exec gzip -9 "{}" \; \
        -exec mv "{}.gz" "{}" \;
}

publish_static_files()
{
    echo "pushing static files to s3://awe-static-files"
    aws --profile awe-publisher s3 cp \
        ${gzipped_static_files_dir} s3://awe-static-files/dist/${version} \
        --recursive \
        --acl public-read \
        --content-encoding gzip \
        --exclude "*.map"
}

main()
{
    echo "Publishing version ${version}"
    validate
    tag
    publish_pypi
    gzip_static_files
    publish_static_files
}

main
