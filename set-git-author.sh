#!/usr/bin/env bash

# # http://stackoverflow.com/a/750191
# # After that, it might be necessary to `git push --force`.

git filter-branch -f --env-filter "
    GIT_AUTHOR_NAME='Raven I. Pilot'
    GIT_AUTHOR_EMAIL='violapterin@gmail.com'
    GIT_COMMITTER_NAME='Raven I. Pilot'
    GIT_COMMITTER_EMAIL='violapterin@gmail.com'
  " HEAD
