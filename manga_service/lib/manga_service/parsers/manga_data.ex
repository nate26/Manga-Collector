defmodule MangaService.Parsers.MangaData do
  alias MangaService.VolumesDB
  alias MangaService.SeriesDB
  alias MangaService.MarketDB
  alias MangaService.ShopsDB
  alias MangaService.CollectionDB

  def get_volume_by_isbn(isbn, user_id) do
    volume = VolumesDB.get_volume_by_isbn(isbn)
    series = SeriesDB.get_series_by_id(volume.series_id)

    market = MarketDB.get_market_by_isbn(isbn)

    shops = ShopsDB.get_shops_by_isbn(isbn)

    collections =
      case user_id do
        nil -> nil
        _ -> CollectionDB.get_collections_by_user_id(%{isbn: isbn, user_id: user_id})
      end

    %{volume: volume, series: series, market: market, shops: shops, collections: collections}
  end

  def get_volume_by_isbn_async(isbn, user_id) do
    tasks = [
      Task.async(fn ->
        volume = VolumesDB.get_volume_by_isbn(isbn)
        series = SeriesDB.get_series_by_id(volume.series_id)
        %{volume: volume, series: series}
      end),
      Task.async(fn -> MarketDB.get_market_by_isbn(isbn) end),
      Task.async(fn -> ShopsDB.get_shops_by_isbn(isbn) end),
      Task.async(fn ->
        case user_id do
          nil -> nil
          _ -> CollectionDB.get_collections_by_user_id(%{isbn: isbn, user_id: user_id})
        end
      end)
    ]

    [volume_data, market, shops, collections] = Task.await_many(tasks)

    %{
      volume: volume_data.volume,
      series: volume_data.series,
      market: market,
      shops: shops,
      collections: collections
    }
  end
end
