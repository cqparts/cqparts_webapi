# cqparts_webapi
A cqparts/cadquery geometry engine

This is a Proof of concept cadquery/cqparts geometry server.

you will need ( this repo )

- gihub.com/zignig/cqparts_bucket

in the same folder as this one , it does a import.

- a working cadquery and cqparts install

- python packages

flask
anytree

run ./serve.py and go to http://localhost:8089/


This is very much alpha , I have _just_ got working , so expect some errors

The intent for this is to provide a geometry api that will generate and cache
on the fly cqparts objects as gltf (and others eventually).

It only exposes numeric properties at the moment, others will follow once
I have had a look at it.


# Docker Setup

Docker is used to build an environment independent of the host, it can then be
used to run, test, and deploy web-page content.


## basis container: `cqparts-env:ubuntu-py3`

Build the `cqparts-env:ubuntu-py3` container from cqparts.

In any directory

```bash
git clone git@github.com:cqparts/cqparts.git
cd cd cqparts/env/ubuntu-py3
./build.sh
```

> FIXME: combine this dependency into the core container
> Why?: honestly, I've done all this work on an LTE network, so i couldn't be
> downloading FreeCAD every time I made a change to the container.

## Populate environment `python-lib`

Follow instructions in [env/python-lib](./env/python-lib) to provide
the libraries the `cqparts_webapi` needs locally.

## Build Container

```bash
cd env/dev
./build.sh
```

## Running Container

```bash
cd env/dev
./run.sh
```
