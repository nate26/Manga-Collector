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

alias MangaService.Volumes

volumes_path = "priv/repo/volumes.json"

volumes_path
|> File.read!()
|> Jason.decode!()
|> Enum.each(fn {_key, volume} ->
  new_vol = %{
    isbn: volume["isbn"],
    brand: volume["brand"],
    series: volume["series"],
    series_id: volume["series_id"],
    edition: nil,
    edition_id: nil,
    display_name: volume["display_name"],
    name: volume["name"],
    category: volume["category"],
    volume: volume["volume"],
    url: volume["url"],
    release_date: volume["release_date"],
    publisher: volume["publisher"],
    format: volume["format"],
    pages: volume["pages"],
    authors: volume["authors"],
    isbn_10: volume["isbn_10"],
    primary_cover_image: hd(volume["cover_images"])["url"],
    cover_images: tl(volume["cover_images"]),
    description: volume["description"]
  }
  IO.puts("Inserting volume: #{new_vol[:isbn]}")
  IO.puts("#{byte_size(new_vol[:description])}")
  case Volumes.create_volume(new_vol) do
    {:ok, _volume} -> :ok
    {:error, _changeset} -> :duplicate
  end
end)
