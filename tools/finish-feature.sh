#!/usr/bin/env bash

set -eu
set -o pipefail

current_branch="$(git symbolic-ref --short HEAD)"
master_branch="master"


main()
{
    git checkout ${master_branch}
    git rebase ${current_branch}
    git push
    git branch -d ${current_branch}
    git push origin :${current_branch}
}

main
