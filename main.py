from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.config import app_host, origins
from data_base.pg_bd import sql_start, sql_close, read_requests, read_activ_requests
from fastapi.responses import JSONResponse


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    await sql_start()


@app.on_event("shutdown")
async def shutdown_event():
    await sql_close()


@app.get('/api/v1/cms_list')
async def get_cms_list():
    data_db = await read_requests()
    data = []
    for db_line in data_db:
        data.append(dict(db_line))

    # Преобразуйте список словарей в JSON
    # json_data = json.dumps(data)
    # Возвращаем список словарей напрямую, без использования json.dumps()
    return JSONResponse(content=data, media_type='application/json')


@app.get('/api/v1/cms_activ')
async def get_cms_list():
    data_db = await read_activ_requests()
    data = []
    for db_line in data_db:
        data.append(dict(db_line))

    # Преобразуйте список словарей в JSON
    # json_data = json.dumps(data)
    # Возвращаем список словарей напрямую, без использования json.dumps()
    return JSONResponse(content=data, media_type='application/json')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host=app_host, port=80, reload=True)
