defmodule MangaServiceWeb.BrowseOptionsController do
  use Phoenix.Controller, formats: [:json]

  alias MangaService.ShopsDB
  alias MangaService.SeriesDB

  def index(conn, _params) do
    promotions = ShopsDB.distinct("promotion")
    genres = SeriesDB.distinct_genres()

    json(
      conn,
      %{
        promotions: promotions,
        genres: genres
      }
    )
  end
end
