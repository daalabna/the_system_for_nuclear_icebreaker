from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from backend.models import (VesselModel, IcebreakerModel, BaseNode, BaseEdge, Template,
                            VesselPath, PostCalcPath, PostCalcPathIce)
from datetime import datetime
from backend.calc.base_graph import BaseGraph
from backend.data.vessels_data import vessels_data, icebreaker_data
from backend.calc.vessel import Vessel, IceBreaker
from backend.crud.crud_types import TemplatesCRUD, VesselPathCRUD
from backend.calculate_timetable import computator, ice_cond
from backend.calc.context import Context
from backend.utils import replace_inf_nan
import json

app = FastAPI()

@app.middleware("http")
async def replace_inf_middleware(request, call_next):
    response = await call_next(request)
    if response.media_type == "application/json":
        body = await response.body()
        content = json.loads(body)
        processed_content = replace_inf_nan(content)
        response = JSONResponse(content=processed_content)
    return response

@app.get("/get_base_nodes/", response_model=List[BaseNode])
async def get_nodes():
    graph = BaseGraph()
    graph.set_base_values()
    return JSONResponse(jsonable_encoder(graph.make_list_of_models_for_nodes()))

@app.get("/get_base_edges/", response_model=List[BaseEdge])
async def get_edges():
    graph = BaseGraph()
    graph.set_base_values()
    return JSONResponse(jsonable_encoder(graph.make_list_of_models_for_edges()))

@app.get("/vessels/", response_model = VesselModel | List[VesselModel])
async def get_vessel(id: int | None = None):

    if not id:
        vessels = [Vessel.make_model_from_dict_entry(id, vessels_data[id]) for id in vessels_data]
        return JSONResponse(jsonable_encoder(vessels))

    if id in vessels_data:
        return JSONResponse(jsonable_encoder(Vessel.make_model_from_dict_entry(id, vessels_data[id])))

    raise HTTPException(status_code=404, detail="Vessel not found")


@app.get("/icebreakers/", response_model = IcebreakerModel | List[IcebreakerModel])
async def get_icebreaker(id: int | None = None):
    if not id:
        icebreakers = [IceBreaker.make_model_from_dict_entry(id, icebreaker_data[id]) for id in icebreaker_data]
        return JSONResponse(jsonable_encoder(icebreakers))

    if id in icebreaker_data:
        return JSONResponse(jsonable_encoder(IceBreaker.make_model_from_dict_entry(id, icebreaker_data[id])))

    raise HTTPException(status_code=404, detail="Vessel not found")


@app.get("/template/", response_model=Template)
async def get_template(template_name: str = ""):
    """
    Получение шаблона по имени
    """
    crud = TemplatesCRUD()
    if template_name:
        return JSONResponse(jsonable_encoder(crud.get(template_name)))
    else:
        return JSONResponse(jsonable_encoder(crud.get_all()))

@app.delete("/template/", response_model=Template)
async def delete_template(template_name: str):
    """
        Удаление шаблона
    """
    crud = TemplatesCRUD()
    return JSONResponse(jsonable_encoder(crud.delete(template_name)))

@app.post("/template/", response_model=Template)
async def post_template(template: Template):
    """
        Публикация шаблона
    """
    crud = TemplatesCRUD()
    # TODO: добавить проверку на корректность идентификаторов ледоколов и судов, пока пох
    return JSONResponse(jsonable_encoder(crud.post(template)))


@app.post("/calculation_request/", response_model=Template)
async def post_calculation_request(template_name: str):
    """
    Заявка на расчет по шаблону template_name
    """
    template: Template =  TemplatesCRUD().get(template_name)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    context = Context().load_from_template_obj(template)
    computator.optimal_timesheet(context)\

@app.get("/calculation_request/", response_model=Template)
async def get_calculation_request_results(template_name: str, vessel_id: int | None = None):
    """
    Получение результатов расчета для судна vessel_id по шаблону template_name
    """
    template: Template =  TemplatesCRUD().get(template_name)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    crud = VesselPathCRUD()

    filter_conds = {"template_name": template_name}

    if vessel_id:
        filter_conds["vessel_id"] = vessel_id

    return JSONResponse(replace_inf_nan(jsonable_encoder(crud.get_by_filter_conds(filter_conds))))


@app.post("/calculate_path_wo_icebreaker/", response_model=VesselPath)
async def calculate_path_wo_icebreaker(vessel_id: int | None = None):
    """
        Получение пути без ледокола для судна vessel_id
    """
    crud = VesselPathCRUD()
    filter_conds = {"template_name": "solo"}

    if vessel_id:
        filter_conds["vessel_id"] = vessel_id

    return JSONResponse(replace_inf_nan(jsonable_encoder(crud.get_by_filter_conds(filter_conds))))


@app.get("/calculate_path_with_icebreaker/", response_model=VesselPath)
async def calculate_path_with_icebreaker(vessel_id: int | None = None):
    """
        Получение пути с лучшим ледоколом для судна vessel_id
    """
    crud = VesselPathCRUD()
    filter_conds = {"template_name": "best"}

    if vessel_id:
        filter_conds["vessel_id"] = vessel_id

    return JSONResponse(replace_inf_nan(jsonable_encoder(crud.get_by_filter_conds(filter_conds))))

@app.get("/get_tiff_name/", response_model=datetime)
async def get_tiff_name(dt: datetime):
    """
    Получение имени файла с тифом (ближайшего к дате прогноза) по дате dt
    """
    return ice_cond.find_appropriate_conditions_date(list(ice_cond.dfs.keys()), dt)

#if __name__ == "__main__":
#    import uvicorn
#    uvicorn.run(app, host="0.0.0.0", port=8003)