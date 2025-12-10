from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import require_user
from app import models
from app.logic.student_manager import StudentManager
from app.logic.algorithms.sorting import SortingAlgorithms
from app.logic.algorithms.searching import SearchingAlgorithms
import json

from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import require_user
from app import models
from app.logic.student_manager import StudentManager
from app.logic.algorithms.sorting import SortingAlgorithms
from app.logic.algorithms.searching import SearchingAlgorithms
import json

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/sorting")
async def sorting_page(request: Request, user: models.User = Depends(require_user), db: Session = Depends(get_db)):
    mgr = StudentManager(db)
    students = mgr.get_all()
    return templates.TemplateResponse("sorting.html", {
        "request": request,
        "user": user,
        "students": students, 
        "active_page": "sorting"
    })

@router.post("/sorting/run")
async def run_sorting(
    request: Request,
    algorithm: str = Form(...),
    sort_key: str = Form(...), # 'nama', 'nim', 'ipk'
    sort_order: str = Form("asc"), # 'asc', 'desc'
    user: models.User = Depends(require_user),
    db: Session = Depends(get_db)
):
    mgr = StudentManager(db)
    students_data = mgr.get_all()
    # Copy list to preserve original order in view if needed (though result will replace it usually)
    data_list = [s for s in students_data] 
    
    result = None
    ascending = (sort_order == "asc")
    
    if algorithm == "bubble":
        result = SortingAlgorithms.bubble_sort(data_list, key=sort_key, ascending=ascending)
    elif algorithm == "selection":
        result = SortingAlgorithms.selection_sort(data_list, key=sort_key, ascending=ascending)
    elif algorithm == "insertion":
        result = SortingAlgorithms.insertion_sort(data_list, key=sort_key, ascending=ascending)
    elif algorithm == "merge":
        result = SortingAlgorithms.merge_sort(data_list, key=sort_key, ascending=ascending)
    elif algorithm == "shell":
        result = SortingAlgorithms.shell_sort(data_list, key=sort_key, ascending=ascending)

    return templates.TemplateResponse("sorting.html", {
        "request": request,
        "user": user,
        "result": result,
        "students": students_data,
        "selected_algorithm": algorithm,
        "selected_key": sort_key,
        "selected_order": sort_order,
        "active_page": "sorting"
    })

@router.get("/searching")
async def searching_page(request: Request, user: models.User = Depends(require_user), db: Session = Depends(get_db)):
    mgr = StudentManager(db)
    students = mgr.get_all()
    return templates.TemplateResponse("searching.html", {
        "request": request,
        "user": user,
        "students": students, 
        "active_page": "searching"
    })

@router.post("/searching/run")
async def run_searching(
    request: Request,
    algorithm: str = Form(...),
    sort_key: str = Form(...), # 'nama', 'nim', 'ipk'
    target_input: str = Form(None),
    user: models.User = Depends(require_user),
    db: Session = Depends(get_db)
):
    mgr = StudentManager(db)
    students_data = mgr.get_all()
    data_list = [s for s in students_data] 
    
    result = None
    
    if not target_input:
         return templates.TemplateResponse("searching.html", {
            "request": request,
            "user": user,
            "students": students_data,
            "error": "Target is required for searching.",
            "selected_algorithm": algorithm,
            "selected_key": sort_key,
            "active_page": "searching"
        })
    
    target = target_input
    if sort_key == "ipk":
        try:
            target = float(target)
        except:
            pass 
    
    if algorithm == "binary":
        # Binary search requires sorted data on the SAME key
        sorted_res = SortingAlgorithms.merge_sort(data_list, key=sort_key, ascending=True)
        data_list = sorted_res.data
        result = SearchingAlgorithms.binary_search(data_list, target, key=sort_key)
    elif algorithm == "linear":
        result = SearchingAlgorithms.linear_search(data_list, target, key=sort_key)
    elif algorithm == "sequential":
        result = SearchingAlgorithms.sequential_search(data_list, target, key=sort_key)
            
    return templates.TemplateResponse("searching.html", {
        "request": request,
        "user": user,
        "result": result,
        "students": students_data, 
        "selected_algorithm": algorithm,
        "selected_key": sort_key,
        "target_input": target_input,
        "active_page": "searching"
    })
