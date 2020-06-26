[![noisycomputation](https://circleci.com/gh/noisycomputation/dash/tree/noisy.svg?style=shield)](https://circleci.com/gh/noisycomputation/dash)

# dash Fork

## Motivation

The only correct way to build the entire dash stack is via the
dash project's circleci build, but that config pulls dash components
from github indiscriminately, making builds of earlier builds impossible
without some fragile config hackery.

Instead, the dash, dash-table, dash-html-components, and dash-core-components
projects have been forked by noisycomputation. The default `noisy` branch of
all the projects points to currently supported mutually-compatible versions
of theproject, and the dash project's circleci config has been modified
to pull in the forks, build them, and publish the resulting packages on
the publicly available python repository <https://noisycomputation.github.io>.
The convention for these forks is to use the very next patch number from
the version on which they are based with a `-a1` suffix:

> Example: upstream v1.2.3 becomes v1.2.4-a1.

The suffix specifies a pre-release of the next patch version consistent with both
Python's [PEP 440](https://www.python.org/dev/peps/pep-0440/#id28) and
Node's [semver](https://github.com/semver/semver/blob/master/semver.md).
The next patch's pre-release was chosen to avoid version conflicts with
upstream, for instance if upstream v1.2.3 were to be forked as v1.2.4,
upstream's subsequent release of v1.2.4 would conflict with the noisycomputation
version.

Projects wishing to use the forked noisycomputation packages need to list the
<https://noisycomputation.github.io>  repository as an extra install URL in
the `pip` vernacular and to pin the dependency to the exact version used by
noisycomputation.

> Care must be taken to list these dependencies *before* any
> other dependencies that might pull the upstream packages. For example, the
> package `dash-bootstrap-components` lists `dash>=1.9.0` as a dependency.
> If the noisycomputation version of `dash` is listed first, it will be
> installed from the noisycomputation repo and will satisfy the
> `dash-bootstrap-components` dependency.

## Build Instructions

Only builds on CircleCI using `.circleci/config.yml` are officially supported.

To make development easier, the circleci environment can be configured locally.
First, fetch the correct CircleCI image (described above in *Fixing Javascript
Dependencies*).

Second, set up a Dockerfile and a build/run script. The script should set up
a bind mount between the hose machine and the Docker container for two directories,
one for the local copy of this dash repo, one for shared files. You may need to
create a user in the Dockerfile and set that user's workdir as the default workdir
in the script; this is because the uid and gid between your user on the host machine
must match that on the client machine for you to have the correct permissions on the
bind-mounted directories (there are other workarounds, like remapping uid and gid, but
this is rather simpler). If a new user is created, add that user to the container's
`/etc/sudoers.d/51-{user_name}` so that the user can escalate privileges. Install vim.

Third, run the container and execute the build, following the CircleCI steps. The
easiest way to do this is to use vim to yank/paste the needed lines into a document
that can be dot-executed from within the container.

## Changes to Upstream

The workflow is to create a new branch from the release that is to be modified:

    git checkout -b noisy_v1.11.0 v1.11.1-a1

Make sure to skip lint verification when comitting:

    git commit --no-verify

The default `noisy` branch merely tracks whichever of the versioned `noisy` branches
is currently in use by noisycomputing. To avoid cluttering the log, point `noisy` to
the appropriate commit as needed and `git push origin --force` without mercy or
concern for the integrity of this repo:

    git branch -vv (note the commit ID of the noisy branch you want to point to)
    git reset --hard {commit ID}
    git push origin --force

#### Changelog (individual version motivations)


* v1.11.1-a1
   The upstream dash-renderer had a small regression introduced in v1.11 and fixed
   in v1.12 where the initial page load would not allow outputs to be actually written
   to on page load. But v1.12 has broken fixed_rows in dash-table, so a custom
   build was required.

   Fix bug that prevents callbacks from updating their outputs on the initial
   firing that happens on page load (see https://github.com/plotly/dash/issues/1223).
   Cherry pick the fix of this particular bug:

      git cherry-pick b4d5846e4

   Modify package.json to pin @babel/core to ^7-9-0 and @babel/preset-env to ^7-9-5
   Need to stay on 1.11 rather than 1.12 due to fixed_rows bug. There are several
   issues open on this, will likely be worked out by next release.

   Need to stay on 1.11 rather than 1.12 due to fixed_rows bug. There are several
   issues open on this, will likely be worked out by next release.

