defmodule MangaServiceWeb.BrowseOptionsController do
  use Phoenix.Controller, formats: [:json]

  alias MangaService.ShopsDB
  alias MangaService.SeriesDB

  def index(conn, _params) do
    stores = ShopsDB.distinct_stores()
    conditions = ShopsDB.distinct_conditions()
    stock_statuses = ShopsDB.distinct_stock_statuses()
    coupons = ShopsDB.distinct_coupons()
    promotions = ShopsDB.distinct_promotions()
    status = SeriesDB.distinct_status()
    category = SeriesDB.distinct_category()
    genres = SeriesDB.distinct_genres()
    themes = SeriesDB.distinct_themes()
    authors = SeriesDB.distinct_authors()
    publishers = SeriesDB.distinct_publishers()

    json(
      conn,
      %{
        stores: stores,
        conditions: conditions,
        stock_statuses: stock_statuses,
        coupons: coupons,
        promotions: promotions,
        status: status,
        category: category,
        genres: genres,
        themes: themes,
        authors: authors,
        publishers: publishers
      }
    )
  end
end
