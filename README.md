# rss-soap-server

A simple server rss reader with javascript client and SOAP communication.

## Dependencies

All dependencies are written in requirements.txt and you can install them with:

```bash
pip install -r requirements.txt
```

You may need to install these libraries for a correct installation of all dependencies:

libxsl1-dev  
libxml2-dev  
postgresql  
postgresql-server-dev  
postgresql-server-dev-all  

**Note**: library refer on Ubuntu package name, please search an equivalent for yours OS.

## How to test

Just type the command below in the main directory:

```bash
honcho start
```

You can see the example page at `http://localhost:5000/` with your browser.  
WSDL generated on `http://localhost:5000/soap?wsdl`.

**Note**: internet connection is required to download jquery library.
**Note**: you must configure a postgresql database. Specification are in `DBSQL.sql` and you must memorize your access credential in `rsspy/config.db`.

## Authors

[Gabriele](https://github.com/Gabriele91)  
[Mirco](https://github.com/MircoT)

## License

Copyright (C) 2013 Gabriele Di Bari, Mirco Tracolli

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
