import asyncio
import azure.functions as func
import numpy as np
from concurrent.futures import ProcessPoolExecutor, Future

app = func.FunctionApp()


@app.route(route="my_trigger", auth_level=func.AuthLevel.ANONYMOUS)
async def my_trigger(req: func.HttpRequest) -> func.HttpResponse:
    with ProcessPoolExecutor() as executor:
        fut: Future[float] = executor.submit(memory_intensive_task_sync)
        norm = await asyncio.wrap_future(fut)

    return func.HttpResponse(body=f'{{ "norm": {norm} }}', status_code=200)


def memory_intensive_task_sync() -> float:
    return asyncio.run(memory_intensive_task_async())


async def memory_intensive_task_async() -> float:
    data = np.random.random_sample((25000, 25000))
    await asyncio.sleep(10)
    norm = np.linalg.norm(data)
    return norm