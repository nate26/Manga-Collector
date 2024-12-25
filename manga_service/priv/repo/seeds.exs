# Script for populating the database. You can run it as:
#
#     mix run priv/repo/seeds.exs
#
# Inside the script, you can read and write to any of your
# repositories directly:
#
#     MangaService.Repo.insert!(%MangaService.SomeSchema{})
#
# We recommend using the bang functions (`insert!`, `update!`
# and so on) as they will fail if something goes wrong.

# region Volumes
# alias MangaService.VolumesDB
# volumes_path = "priv/repo/volumes.json"

# volumes_path
# |> File.read!()
# |> Jason.decode!()
# |> Enum.each(fn {_key, volume} ->
#   new_vol = %{
#     isbn: volume["isbn"],
#     brand: volume["brand"],
#     series: volume["series"],
#     series_id: volume["series_id"],
#     edition: nil,
#     edition_id: nil,
#     display_name: volume["display_name"],
#     name: volume["name"],
#     category: volume["category"],
#     volume: volume["volume"],
#     url: volume["url"],
#     release_date: volume["release_date"],
#     publisher: volume["publisher"],
#     format: volume["format"],
#     pages: volume["pages"],
#     authors: volume["authors"],
#     isbn_10: volume["isbn_10"],
#     primary_cover_image: hd(volume["cover_images"])["url"],
#     cover_images: tl(volume["cover_images"]),
#     description: volume["description"]
#   }

#   IO.puts("Inserting volume: #{new_vol[:isbn]}")
#   IO.puts("#{byte_size(new_vol[:description])}")

#   case VolumesDB.create_volume(new_vol) do
#     {:ok, _volume} -> :ok
#     {:error, _changeset} -> :duplicate
#   end
# end)

# endregion Volumes

# region Series
# alias MangaService.SeriesDB
# series_path = "priv/repo/series.json"

# series_path
# |> File.read!()
# |> Jason.decode!()
# |> Map.to_list()
# |> Enum.filter(fn {_key, series} -> !is_nil(series["recommendations"]) end)
# |> Enum.each(fn {_key, series} ->
#   IO.puts("Inserting series: #{series["title"]}")

#   new_series = %{
#     series_id: series["series_id"],
#     title: series["title"],
#     associated_titles: series["associated_titles"],
#     url: series["url"],
#     category: series["category"],
#     series_match_confidence: series["series_match_confidence"],
#     editions: [],
#     volumes: series["volumes"] |> Enum.map(& &1["isbn"]),
#     description: series["description"],
#     cover_image: series["cover_image"],
#     genres: series["genres"],
#     themes: series["themes"],
#     latest_chapter: series["latest_chapter"],
#     release_status: series["release_status"],
#     status: series["status"],
#     authors: series["authors"],
#     publishers: series["publishers"],
#     bayesian_rating: series["bayesian_rating"],
#     rank: series["rank"],
#     recommendations: Enum.map(series["recommendations"], &Integer.to_string/1)
#   }

#   case SeriesDB.create_series(new_series) do
#     {:ok, _series} -> :ok
#     {:error, _changeset} -> :duplicate
#   end
# end)

# endregion Series

# region Market
# alias MangaService.MarketDB
# shop_path = "priv/repo/shop.json"

# shop_path
# |> File.read!()
# |> Jason.decode!()
# |> Enum.each(fn {_key, shop} ->
#   IO.puts("Inserting market: #{shop["isbn"]}")

#   new_shop = %{
#     isbn: shop["isbn"],
#     retail_price: shop["retail_price"]
#   }

#   res =
#     case MarketDB.create_market(new_shop) do
#       {:ok, _market} -> :ok
#       {:error, _changeset} -> :duplicate
#     end

#   IO.puts(res)
# end)

# endregion Market

# region Shops
# alias MangaService.ShopsDB
# shop_path = "priv/repo/shop.json"

# shop_path
# |> File.read!()
# |> Jason.decode!()
# |> Map.to_list()
# |> Enum.each(fn {_key, item} ->
#   IO.puts("Inserting market: #{item["isbn"]}")

#   for shop <- item["shops"] do
#     new_shop = %{
#       item_id: item["isbn"] <> shop["store"] <> shop["condition"],
#       isbn: item["isbn"],
#       store: shop["store"],
#       condition: shop["condition"],
#       url: shop["url"],
#       price: shop["store_price"],
#       stock_status: shop["stock_status"],
#       last_stock_update: shop["last_stock_update"],
#       coupon: shop["coupon"],
#       is_on_sale: shop["is_on_sale"]
#     }

#     res =
#       case ShopsDB.create_shop(new_shop) do
#         {:ok, _shop} -> :ok
#         {:error, changeset} -> changeset
#       end

#     IO.puts(res)
#   end
# end)

# endregion Shops

# region Users
# alias MangaService.UsersDB
# new_user = %{
#   email: "",
#   username: "natevin",
#   password: "",
#   user_id: "",
#   picture: nil,
#   banner: nil,
#   color: nil,
#   theme: nil,
#   personal_stores: []
# }
# res = case UsersDB.create_user(new_user) do
#   {:ok, _user} -> :ok
#   {:error, changeset} -> changeset
# end
# IO.puts(res)
# endregion Users

# region Collections
# alias MangaService.CollectionDB
# collection_path = "priv/repo/collections.json"

# collection_path
# |> File.read!()
# |> Jason.decode!()
# |> Enum.each(fn item ->
#   IO.puts("Inserting collection: #{item["isbn"]}")
#   uc = hd(item["user_collection_data"])

#   new_collection = %{
#     collection_id: uc["id"],
#     read: uc["read"],
#     store: uc["merchant"],
#     collection:
#       case uc["state"] do
#         "Gift" -> "Gift"
#         _ -> "Collection"
#       end,
#     user_id: uc["user_id"],
#     isbn: uc["isbn"],
#     cost: uc["cost"],
#     purchase_date:
#       case String.split(uc["purchaseDate"] || "", "/") do
#         [m, d, y] ->
#           Date.new(String.to_integer(y), String.to_integer(m), String.to_integer(d))
#           |> elem(1)
#           |> Date.to_string()

#         _ ->
#           nil
#       end,
#     tags:
#       case uc["giftToMe"] do
#         true -> ["gift" | uc["tags"] || []]
#         _ -> uc["tags"] || []
#       end,
#     rating: nil
#   }

#   # IO.inspect(new_collection)
#   res =
#     case CollectionDB.create_collection(new_collection) do
#       {:ok, _collection} -> :ok
#       {:error, changeset} -> changeset
#     end

#   IO.puts(res)
# end)

# endregion Collections
