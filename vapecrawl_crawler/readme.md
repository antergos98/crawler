## Execute

```bash
docker run --rm -it -v ./:/code python:3.7 bash
pip install -r requirements.txt
cd /code/vapecrawl_crawler
python run.py
```