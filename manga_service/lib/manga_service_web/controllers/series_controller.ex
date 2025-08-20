defmodule MangaServiceWeb.SeriesController do
  use Phoenix.Controller, formats: [:json]
  alias MangaService.SeriesDB

  def index(conn, _params) do
    all_series = SeriesDB.list_series()

    json(
      conn,
      all_series
      |> Enum.map(fn series ->
        %{
          id: series.id,
          status: series.status,
          description: series.description,
          title: series.title,
          category: series.category,
          url: series.url,
          series_id: series.series_id,
          associated_titles: series.associated_titles,
          series_match_confidence: series.series_match_confidence,
          editions: series.editions,
          volumes: series.volumes,
          cover_image: series.cover_image,
          genres: series.genres,
          themes: series.themes,
          latest_chapter: series.latest_chapter,
          release_status: series.release_status,
          authors: series.authors,
          publishers: series.publishers,
          bayesian_rating: series.bayesian_rating,
          rank: series.rank,
          recommendations: series.recommendations,
          inserted_at: series.inserted_at,
          updated_at: series.updated_at
        }
      end)
    )
  end

  def show(conn, %{"id" => series_id}) do
    series = SeriesDB.get_series_by_id(series_id)

    case series do
      nil ->
        raise "No record found for Series ID"

      _ ->
        json(conn, %{
          id: series.id,
          status: series.status,
          description: series.description,
          title: series.title,
          category: series.category,
          url: series.url,
          series_id: series.series_id,
          associated_titles: series.associated_titles,
          series_match_confidence: series.series_match_confidence,
          editions: series.editions,
          volumes: series.volumes,
          cover_image: series.cover_image,
          genres: series.genres,
          themes: series.themes,
          latest_chapter: series.latest_chapter,
          release_status: series.release_status,
          authors: series.authors,
          publishers: series.publishers,
          bayesian_rating: series.bayesian_rating,
          rank: series.rank,
          recommendations: series.recommendations,
          inserted_at: series.inserted_at,
          updated_at: series.updated_at
        })
    end
  end

  def create(conn, %{"series" => series_params}) do
    case SeriesDB.create_series(series_params) do
      {:ok, series} ->
        conn
        |> put_status(:created)
        |> json(%{
          id: series.id,
          status: series.status,
          description: series.description,
          title: series.title,
          category: series.category,
          url: series.url,
          series_id: series.series_id,
          associated_titles: series.associated_titles,
          series_match_confidence: series.series_match_confidence,
          editions: series.editions,
          volumes: series.volumes,
          cover_image: series.cover_image,
          genres: series.genres,
          themes: series.themes,
          latest_chapter: series.latest_chapter,
          release_status: series.release_status,
          authors: series.authors,
          publishers: series.publishers,
          bayesian_rating: series.bayesian_rating,
          rank: series.rank,
          recommendations: series.recommendations,
          inserted_at: series.inserted_at,
          updated_at: series.updated_at
        })

      {:error, changeset} ->
        conn
        |> put_status(:unprocessable_entity)
        |> json(%{errors: changeset.errors})
    end
  end

  def update(conn, %{"id" => isbn, "series" => series_params}) do
    curr_series = SeriesDB.get_series_by_id(isbn)

    case SeriesDB.update_series(curr_series, series_params) do
      {:ok, series} ->
        conn
        |> put_status(:ok)
        |> json(%{
          id: series.id,
          status: series.status,
          description: series.description,
          title: series.title,
          category: series.category,
          url: series.url,
          series_id: series.series_id,
          associated_titles: series.associated_titles,
          series_match_confidence: series.series_match_confidence,
          editions: series.editions,
          volumes: series.volumes,
          cover_image: series.cover_image,
          genres: series.genres,
          themes: series.themes,
          latest_chapter: series.latest_chapter,
          release_status: series.release_status,
          authors: series.authors,
          publishers: series.publishers,
          bayesian_rating: series.bayesian_rating,
          rank: series.rank,
          recommendations: series.recommendations,
          inserted_at: series.inserted_at,
          updated_at: series.updated_at
        })

      {:error, changeset} ->
        conn
        |> put_status(:unprocessable_entity)
        |> json(%{errors: changeset.errors})
    end
  end

  def delete(conn, %{"id" => series_id}) do
    series = SeriesDB.get_series_by_id(series_id)

    case SeriesDB.delete_series(series) do
      {:ok, _} ->
        conn
        |> put_status(:ok)
        |> json(%{success: true})

      {:error, _} ->
        conn
        |> put_status(:unprocessable_entity)
        |> json(%{errors: "Unable to delete series"})
    end
  end
end
