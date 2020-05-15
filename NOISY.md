# dash Fork

## Motivation

The upstream dash-renderer had a small regression introduced in v1.11 and fixed
in v1.12 where the initial page load would not allow outputs to be actually written
to on page load. But v1.12 has broken fixed_rows in dash-table, so a custom
build was required.

## Build Instructions

First, set up the environment correctly.

* Create an outer directory, called something like dash-env, and move
  the cloned dash-table directory into it.
* In the outer directory, create a python + node virtualenv:
    
    ```
    python -m venv venv
    source venv/bin/activate
    pip install -U pip; pip install nodeenv
    nodeenv -p
    ```

Make sure you have the correct branch checked out and build:

* cd dash-renderer (if building only dash-renderer)
* npm install
* npm run private::build:js
* python setup.py sdist

If the javascript build results in errors, often these are caused by incorrect version
pinning in package.json. @babel/core and @babel/preset-env are frequent culprits, try
pinning to 7-9-0 and 7-9-5, respectively, and re-run `npm install`.

The output package will be in the `dist` directory. This is ready to be installed with
pip.

## Changes to Upstream

The workflow is to create a new branch from the release that is to be modified:

    git checkout -b noisy_v1.11 v1.11

Make sure to skip lint verification when comitting:

    git commit --no-verify

The default `noisy` branch merely tracks whichever of the versioned `noisy` branches
is currently in use by noisycomputing. To avoid cluttering the log, point `noisy` to
the appropriate commit as needed and `git push origin --force` without mercy or
concern for the integrity of this repo:

    git branch -vv (note the commit ID of the noisy branch you want to point to)
    git reset --hard {commit ID}
    git push origin --force

#### Changelog


* v1.11

   Fix bug that prevents callbacks from updating their outputs on the initial
   firing that happens on page load (see https://github.com/plotly/dash/issues/1223).
   Cherry pick the fix of this particular bug:

      git cherry-pick b4d5846e4

   Modify package.json to pin @babel/core to ^7-9-0 and @babel/preset-env to ^7-9-5
   Need to stay on 1.11 rather than 1.12 due to fixed_rows bug. There are several
   issues open on this, will likely be worked out by next release.

   Need to stay on 1.11 rather than 1.12 due to fixed_rows bug. There are several
   issues open on this, will likely be worked out by next release.

