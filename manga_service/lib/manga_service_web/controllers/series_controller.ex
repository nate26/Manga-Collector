defmodule MangaServiceWeb.SeriesController do
  use Phoenix.Controller, formats: [:json]
  use Timex
  alias MangaService.SeriesDB

  defp parse_date(date) do
    case date do
      nil ->
        DateTime.new(~D[1000-01-01], ~T[00:00:00])

      _ ->
        DateTime.new(date, ~T[00:00:00])
    end
    |> elem(1)
  end

  defp map_volumes(volume_details) do
    volume_details
    |> Enum.map(fn v ->
      %{
        isbn: v.isbn,
        name: v.name,
        category: v.category,
        volume: v.volume,
        # TODO stock_status: v.stock_status,
        release_date: v.release_date,
        url: v.url,
        primary_cover_image: v.primary_cover_image,
        format: v.format
      }
    end)
    |> Enum.sort(fn a, b ->
      case DateTime.compare(
             parse_date(a.release_date),
             parse_date(b.release_date)
           ) do
        :gt -> false
        _ -> true
      end
    end)
  end

  def index(conn, params) do
    all_series = SeriesDB.list_series(params)

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
          volumes: map_volumes(series.volume_details),
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
          volumes: map_volumes(series.volume_details),
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
          volumes: map_volumes(series.volume_details),
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
