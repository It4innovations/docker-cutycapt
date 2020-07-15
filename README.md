# docker-cutycapt

Latest Debian with cutycapt based on repos:

* https://github.com/marazmiki/docker-flaskycapt

You can request the API

```console
curl -H 'Content-Type: application/json' -d '{"url": "http://www.it4i.cz"}' http://localhost:5000/thumbnail -o out.png
```

The thumbnail endpoint accepts only application/json content type, so request body should be a valid JSON.

Available arguments:

* **url** - The URL to capture
* **min_width** - Minimal width for the image (default: 1680)
* **min_height** - Minimal height for the image (default: 1280)
* **delay** - After successful load, wait miliseconds (default: 0)
* **out_format** - The target file (.png|jpg|...)
* **max_wait** - Don't wait more than miliseconds (default: 16000, inf: 0)
* **resize** - Geometry resize the image (300|x300|...)
