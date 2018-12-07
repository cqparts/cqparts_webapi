# Python Libraries for Test

Any modules stored in this folder will be imported before anything installed
in the test environments.

**Typical Libraries**

At the time of writing this [2018-12], I've had success linking the following
repositories in:

```bash
# Cloning repositories
mkdir _repos
pushd _repos
git clone https://github.com/zignig/cqparts_bucket
git clone git@github.com:cqparts/cqparts.git
popd

# Symlinking repos internals
ln -s _repos/cqparts_bucket .
#ln -s _repos/cqparts/src/cqparts .
ln -s _repos/cqparts/src/cqparts_bearings .
ln -s _repos/cqparts/src/cqparts_bucket .
ln -s _repos/cqparts/src/cqparts_fasteners .
ln -s _repos/cqparts/src/cqparts_gears .
ln -s _repos/cqparts/src/cqparts_misc .
ln -s _repos/cqparts/src/cqparts_motors .
ln -s _repos/cqparts/src/cqparts_toys .
```

## `cadquery` as an example

The parallel development of the `cadquery` library with `cqparts` has been
necessary for early stages of developing `cqparts`, this is how testing is done
with different sources of `cadquery`

### `cadquery` installed from `pip`

With no additions to the `python-lib` folder, we can run the following commands
to see that the default imported `cadquery` version has been installed in the
docker image.

Running a python console inside the `dev` environment, with `$CWD` as
this `python-lib` folder:

    $ cd dev
    $ ./run.sh python
    Python 3.5.2 (default, Nov 23 2017, 16:37:01)
    [GCC 5.4.0 20160609] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import cadquery
    >>> cadquery
    <module 'cadquery' from '/usr/local/lib/python2.7/dist-packages/cadquery/__init__.pyc'>

### Custom `cadquery` branch

If we wish to use a specific branch from the `cadquery` (or in fact any
fork of that repository), we can add it to this `python-lib` folder

Adding the `cadquery` repository, let's put it into a sub-folder:

    $ mkdir _repos
    $ cd _repos

    # clone the repo into a "cadquery" folder, with "master" checked out
    $ git clone git@github.com:dcowden/cadquery.git

    $ cd .. # back to the python-lib folder

    # create a cadquery symlink to the module inside the repository
    $ ln -s _repos/cadquery/cadquery cadquery

Gives us the directory structure:

    .
    ├── cadquery -> _repos/cadquery/cadquery (the symlink we created)
    ├── README.md (this file)
    └── _repos
        └── cadquery ("master" branch, or whatever you decide to checkout)
            ├── ... truncated
            └── cadquery
                ├── ... truncated
                └── __init__.py

Now we can re-run the above commands (streamlined into one line) to show that
we're now picking up the `cadquery` library from our github repository clone:

    $ cd dev
    $ ./run.sh python -c 'import cadquery; print(cadquery)'
    <module 'cadquery' from '/code/tests/env/python-lib/cadquery/__init__.pyc'>
