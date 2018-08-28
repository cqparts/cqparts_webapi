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

The intent for this is to provide a geometry api that will generate and cache on the fly cqparts objects as gltf (and others eventually).

It only exposes numeric properties at the moment, others will follow once I have had a look at it.

 
