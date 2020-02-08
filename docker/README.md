# Flask bbt_shop

# Usage

Run as a normal docker and mount your project to `/project`.

Use the following environment variable to select runing mode:
`APP_MODE=development|production`


> build

`cd /<path>/docker`

`docker build bbt_shop:latest .`

> run production

`docker run -d --name bbt_prod -p 5001:5000 -v /data/bbt/bbt_backend:/project -e APP_MODE=production bbt_shop:latest`

> run dev

`docker run -d --name bbt_dev -p 5002:5000 -v /data/bbt/bbt_backend:/project -e APP_MODE=development bbt_shop:latest`