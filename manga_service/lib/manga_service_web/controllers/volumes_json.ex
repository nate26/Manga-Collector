defmodule MangaServiceWeb.VolumesJSON do
  alias MangaService.VolumesDB.Volume

  def index(%{volumes: volumes}) do
    %{data: for(volume <- volumes, do: data(volume))}
  end

  # def show(%{volume: volume}) do
  #   case volume do
  #     nil -> raise "No record found for ISBN"
  #     _ -> %{data: data(volume)}
  #   end
  # end

  defp data(%Volume{} = datum) do
    %{
      id: datum.id,
      name: datum.name,
      format: datum.format,
      description: datum.description,
      category: datum.category,
      url: datum.url,
      isbn: datum.isbn,
      brand: datum.brand,
      series: datum.series,
      series_id: datum.series_id,
      edition: datum.edition,
      edition_id: datum.edition_id,
      display_name: datum.display_name,
      volume: datum.volume,
      release_date: datum.release_date,
      publisher: datum.publisher,
      pages: datum.pages,
      authors: datum.authors,
      isbn_10: datum.isbn_10,
      primary_cover_image: datum.primary_cover_image,
      cover_images: datum.cover_images,
      inserted_at: datum.inserted_at,
      updated_at: datum.updated_at
    }
  end

  def get(%{volume: volume, series: series, market: market, shops: shops, collection: collection}) do
    case volume do
      nil ->
        raise "No record found for ISBN"

      _ ->
        %{
          id: volume.id,
          name: volume.name,
          format: volume.format,
          description: volume.description,
          category: volume.category,
          url: volume.url,
          isbn: volume.isbn,
          brand: volume.brand,
          series: volume.series,
          series_id: volume.series_id,
          edition: volume.edition,
          edition_id: volume.edition_id,
          display_name: volume.display_name,
          volume: volume.volume,
          release_date: volume.release_date,
          publisher: volume.publisher,
          pages: volume.pages,
          authors: volume.authors,
          isbn_10: volume.isbn_10,
          primary_cover_image: volume.primary_cover_image,
          cover_images: volume.cover_images,
          inserted_at: volume.inserted_at,
          updated_at: volume.updated_at,
          series_data: %{
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
          },
          market: %{
            isbn: market.isbn,
            retail_price: market.retail_price,
            inserted_at: market.inserted_at,
            updated_at: market.updated_at
          },
          shops:
            shops
            |> Enum.map(fn shop ->
              %{
                item_id: shop.item_id,
                store: shop.store,
                url: shop.url,
                condition: shop.condition,
                price: shop.price,
                stock_status: shop.stock_status,
                last_stock_update: shop.last_stock_update,
                coupon: shop.coupon,
                is_on_sale: shop.is_on_sale,
                inserted_at: shop.inserted_at,
                updated_at: shop.updated_at
              }
            end),
          collection:
            collection
            |> case do
              nil ->
                nil

              collections ->
                collections
                |> Enum.map(fn collection ->
                  %{
                    user_id: collection.user_id,
                    collection_id: collection.collection_id,
                    read: collection.read,
                    store: collection.store,
                    collection: collection.collection,
                    cost: collection.cost,
                    purchase_date: collection.purchase_date,
                    tags: collection.tags,
                    rating: collection.rating,
                    inserted_at: collection.inserted_at,
                    updated_at: collection.updated_at
                  }
                end)
            end
        }
    end
  end
end
