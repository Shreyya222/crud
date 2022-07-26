from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import Movie, MovieUpdate

router = APIRouter()

@router.post("/", response_description="Create a new movie", status_code=status.HTTP_201_CREATED, response_model=Movie)
def create_movie(request: Request, movie: Movie = Body(...)):
    movie = jsonable_encoder(movie)
    new_movie = request.app.database["movies"].insert_one(movie)
    created_movie = request.app.database["movies"].find_one(
        {"_id": new_movie.inserted_id}
    )

    return created_movie


@router.get("/", response_description="List all movies", response_model=List[Movies])
def list_movies(request: Request):
    movies = list(request.app.database["movies"].find(limit=100))
    return movies

    
@router.get("/{id}", response_description="Get a single movie by id", response_model=Movie)
def find_movie(id: str, request: Request):
    if (movie := request.app.database["movies"].find_one({"_id": id})) is not None:
        return movie

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID {id} not found"


@router.put("/{id}", response_description="Update a movie", response_model=Movie)
def update_movie(id: str, request: Request, movie: MovieUpdate = Body(...)):
    movie = {k: v for k, v in movie.dict().items() if v is not None}

    if len(movie) >= 1:
        update_result = request.app.database["movies"].update_one(
            {"_id": id}, {"$set": movie}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID {id} not found")

              if (
        existing_movie := request.app.database["movies"].find_one({"_id": id})
    ) is not None:
        return existing_movie

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID {id} not found")


@router.delete("/{id}", response_description="Delete a movie")
def delete_movie(id: str, request: Request, response: Response):
    delete_result = request.app.database["movies"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Mobie with ID {id} not found")